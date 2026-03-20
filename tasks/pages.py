from os import environ

from shared.timed_page import TimedPage

from .models import TASKS, Player, Constants


def current_task(player: Player):
    return TASKS[player.task_id]


def debug_context(player: Player):
    return dict(
        show_debug_treatment=environ.get('OTREE_PRODUCTION') != '1',
        debug_treatment=player.treatment,
    )


class PreAnswerPage(TimedPage):
    """Page 1: Scenario + pre-answer + pre-confidence"""
    form_model = 'player'

    def get_form_fields(self):
        return ['pre_numeric_response', 'pre_confidence']

    def vars_for_template(self):
        task = current_task(self.player)
        return dict(
            task=task,
            round_number=self.round_number,
            total_rounds=Constants.num_rounds,
            **debug_context(self.player),
        )

    def error_message(self, values):
        value = values['pre_numeric_response']
        if self.player.task_id == 'time_preference' and not 75 <= value <= 200:
            return 'Please enter an amount between 75 and 200 USD.'
        if self.player.task_id in ('dictator', 'trolley', 'gneezy_potters') and not 0 <= value <= 100:
            return 'Please enter a number between 0 and 100.'


class LLMAdvicePage(TimedPage):
    """Page 2: LLM interaction (Ask AI + streaming response)"""
    form_model = 'player'
    form_fields = [
        'io_history',
        'interrupt_latency_submit',
        'interrupt_latency_stream',
        'interrupted_stream',
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
            llm_output=task['llm_output'],
        )

    @staticmethod
    def live_method(player, data):
        return {player.id_in_group: dict(output=TASKS[player.task_id]['llm_output'], input=data.get('input', ''))}


class RevisedAnswerPage(TimedPage):
    """Page 3: Revised answer + post self-confidence"""
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


class MechanismMeasuresPage(TimedPage):
    """Page 4: Cognitive trust, affective trust, confidence in AI"""
    form_model = 'player'
    form_fields = [
        'post_confidence',
        'cognitive_trust',
        'affective_trust',
        'confidence_in_ai',
    ]

    def vars_for_template(self):
        task = current_task(self.player)
        return dict(task=task, **debug_context(self.player))


page_sequence = [
    PreAnswerPage,
    LLMAdvicePage,
    RevisedAnswerPage,
    MechanismMeasuresPage,
]
