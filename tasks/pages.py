from shared.timed_page import TimedPage

from .models import TASKS, Player, Constants


def current_task(player: Player):
    return TASKS[player.task_id]


class TaskIntroPage(TimedPage):
    def vars_for_template(self):
        task = current_task(self.player)
        return dict(
            task=task,
            round_number=self.round_number,
            total_rounds=Constants.num_rounds,
        )


class PreInteractionTaskPage(TimedPage):
    form_model = 'player'

    def get_form_fields(self):
        task_type = current_task(self.player)['response_type']
        if task_type == 'numeric':
            return ['pre_numeric_response']
        if task_type == 'choice':
            return ['pre_choice_response']
        return ['pre_alloc_stocks', 'pre_alloc_bonds', 'pre_alloc_cash']

    def vars_for_template(self):
        task = current_task(self.player)
        return dict(task=task, stage_title='Before seeing LLM advice')

    def error_message(self, values):
        task = current_task(self.player)
        if task['response_type'] == 'numeric':
            value = values['pre_numeric_response']
            if self.player.task_id == 'ultimatum' and not 0 <= value <= 1000:
                return 'Your ultimatum offer must be between 0 and 1000 USD.'
            if self.player.task_id == 'dictator' and not 0 <= value <= 100:
                return 'Your dictator allocation must be between 0 and 100 USD.'
            if self.player.task_id == 'trolley' and not 0 <= value <= 100:
                return 'Your trolley response must be between 0 and 100.'
        if task['response_type'] == 'allocation':
            total = values['pre_alloc_stocks'] + values['pre_alloc_bonds'] + values['pre_alloc_cash']
            if total != 10000:
                return 'Your stock, bond, and cash allocations must sum to exactly 10000 USD.'


class LLMInteraction(TimedPage):
    form_model = 'player'
    form_fields = [
        'io_history',
        'interrupt_latency_submit',
        'interrupt_latency_stream',
        'interrupted_stream',
        'reflection_time',
    ]

    def vars_for_template(self):
        task = current_task(self.player)
        return dict(task=task, llm_interaction_instructions=task['llm_instruction'])

    def js_vars(self):
        task = current_task(self.player)
        return dict(
            treatment=self.player.treatment,
            llm_output=task['llm_output'],
            llm_interaction_attempts=1,
        )

    @staticmethod
    def live_method(player, data):
        return {player.id_in_group: dict(output=TASKS[player.task_id]['llm_output'], input=data.get('input', ''))}


class PostInteractionTaskPage(TimedPage):
    form_model = 'player'

    def get_form_fields(self):
        task_type = current_task(self.player)['response_type']
        if task_type == 'numeric':
            return ['post_numeric_response']
        if task_type == 'choice':
            return ['post_choice_response']
        return ['post_alloc_stocks', 'post_alloc_bonds', 'post_alloc_cash']

    def vars_for_template(self):
        task = current_task(self.player)
        return dict(task=task, stage_title='After seeing LLM advice')

    def error_message(self, values):
        task = current_task(self.player)
        if task['response_type'] == 'numeric':
            value = values['post_numeric_response']
            if self.player.task_id == 'ultimatum' and not 0 <= value <= 1000:
                return 'Your ultimatum offer must be between 0 and 1000 USD.'
            if self.player.task_id == 'dictator' and not 0 <= value <= 100:
                return 'Your dictator allocation must be between 0 and 100 USD.'
            if self.player.task_id == 'trolley' and not 0 <= value <= 100:
                return 'Your trolley response must be between 0 and 100.'
        if task['response_type'] == 'allocation':
            total = values['post_alloc_stocks'] + values['post_alloc_bonds'] + values['post_alloc_cash']
            if total != 10000:
                return 'Your stock, bond, and cash allocations must sum to exactly 10000 USD.'


class TaskMeasuresPage(TimedPage):
    form_model = 'player'
    form_fields = [
        'retention_q1',
        'retention_q2',
        'llm_reliance',
        'llm_confidence_post',
        'llm_helpfulness',
        'llm_usefulness',
        'llm_trustworthiness',
        'llm_understanding',
        'llm_future_use_likelihood',
        'llm_use_again',
    ]

    def vars_for_template(self):
        task = current_task(self.player)
        return dict(
            task=task,
            retention_q1_text=task['retention_q1_text'],
            retention_q2_text=task['retention_q2_text'],
        )


page_sequence = [
    TaskIntroPage,
    PreInteractionTaskPage,
    LLMInteraction,
    PostInteractionTaskPage,
    TaskMeasuresPage,
]
