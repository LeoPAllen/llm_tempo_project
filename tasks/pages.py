from os import environ

from shared.timed_page import TimedPage

from .models import (
    Player,
    STREAM_DELAYS_MS,
    get_active_task_ids,
    get_task_definition,
    is_study_1_session,
)


def current_task(player: Player):
    return get_task_definition(player)


def is_active_task_round(player: Player):
    return bool(player.task_id)


def debug_context(player: Player):
    return dict(
        show_debug_treatment=environ.get('OTREE_PRODUCTION') != '1',
        debug_treatment=player.treatment,
    )


class ActiveTaskPage(TimedPage):
    def is_displayed(self):
        return super().is_displayed() and is_active_task_round(self.player)


class PreAnswerPage(ActiveTaskPage):
    """Page 1: Scenario + pre-answer + pre-confidence"""
    template_name = 'tasks/PreAnswerPage.html'
    form_model = 'player'

    def get_form_fields(self):
        return ['pre_numeric_response', 'pre_confidence']

    def vars_for_template(self):
        task = current_task(self.player)
        return dict(
            task=task,
            round_number=self.round_number,
            total_rounds=len(get_active_task_ids(self.session)),
            **debug_context(self.player),
        )

    def error_message(self, values):
        value = values['pre_numeric_response']
        if self.player.task_id == 'time_preference' and not 75 <= value <= 200:
            return 'Please enter an amount between 75 and 200 USD.'
        if self.player.task_id in ('dictator', 'trolley', 'gneezy_potters') and not 0 <= value <= 100:
            return 'Please enter a number between 0 and 100.'


class LLMAdvicePage(ActiveTaskPage):
    """Page 2: LLM interaction (Ask AI + streaming response)"""
    template_name = 'tasks/LLMAdvicePage.html'
    form_model = 'player'
    form_fields = [
        'io_history',
        'interrupt_latency_submit',
        'interrupt_latency_stream',
        'interrupted_stream',
        'advice_page_loaded_at_ms',
        'advice_stream_started_at_ms',
        'advice_stream_ended_at_ms',
        'advice_next_clicked_at_ms',
        'advice_elapsed_load_to_next_ms',
        'advice_elapsed_stream_end_to_next_ms',
    ]

    def vars_for_template(self):
        task = current_task(self.player)
        return dict(
            task=task,
            llm_prompt=task['llm_prompt'],
            **debug_context(self.player),
        )

    def js_vars(self):
        task = current_task(self.player)
        return dict(
            treatment=self.player.treatment,
            stream_delay_ms=STREAM_DELAYS_MS.get(
                self.player.treatment, STREAM_DELAYS_MS['fast_stream']
            ),
            llm_output=task['llm_output'],
        )

    @staticmethod
    def live_method(player, data):
        task = current_task(player)
        return {
            player.id_in_group: dict(
                output=task['llm_output'], input=data.get('input', '')
            )
        }

    def before_next_page(self):
        super().before_next_page()
        loaded_at = self.player.advice_page_loaded_at_ms
        stream_ended_at = self.player.advice_stream_ended_at_ms
        next_clicked_at = self.player.advice_next_clicked_at_ms

        if loaded_at and next_clicked_at and not self.player.advice_elapsed_load_to_next_ms:
            self.player.advice_elapsed_load_to_next_ms = max(
                0, next_clicked_at - loaded_at
            )
        if (
            stream_ended_at
            and next_clicked_at
            and not self.player.advice_elapsed_stream_end_to_next_ms
        ):
            self.player.advice_elapsed_stream_end_to_next_ms = max(
                0, next_clicked_at - stream_ended_at
            )


class RevisedAnswerPage(ActiveTaskPage):
    """Page 3: Revised answer + post self-confidence"""
    template_name = 'tasks/RevisedAnswerPage.html'
    form_model = 'player'

    def get_form_fields(self):
        return ['post_numeric_response']

    def vars_for_template(self):
        task = current_task(self.player)
        return dict(
            task=task,
            pre_response=self.player.pre_numeric_response,
            **debug_context(self.player),
        )

    def error_message(self, values):
        value = values['post_numeric_response']
        if self.player.task_id == 'time_preference' and not 75 <= value <= 200:
            return 'Please enter an amount between 75 and 200 USD.'
        if self.player.task_id in ('dictator', 'trolley', 'gneezy_potters') and not 0 <= value <= 100:
            return 'Please enter a number between 0 and 100.'


class MechanismMeasuresPage(ActiveTaskPage):
    """Page 4: Task-level mechanism measures"""
    template_name = 'tasks/MechanismMeasuresPage.html'
    form_model = 'player'

    def get_form_fields(self):
        fields = [
            'post_confidence',
            'cognitive_trust',
            'affective_trust',
            'confidence_in_ai',
        ]
        if is_study_1_session(self.session):
            fields.extend([
                'cognitive_tax_mental_effort',
                'cognitive_tax_follow_easy',
                'cognitive_tax_mental_fatigue',
                'labor_illusion_effort',
                'labor_illusion_expertise',
                'labor_illusion_thoroughness',
            ])
        return fields

    def vars_for_template(self):
        task = current_task(self.player)
        return dict(
            task=task,
            is_study_1=is_study_1_session(self.session),
            **debug_context(self.player),
        )


page_sequence = [
    PreAnswerPage,
    LLMAdvicePage,
    RevisedAnswerPage,
    MechanismMeasuresPage,
]
