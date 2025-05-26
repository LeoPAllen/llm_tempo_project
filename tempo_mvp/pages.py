from otree.api import Page
from .models import Constants

class PriorBeliefsPage(Page):
    form_model = 'player'
    form_fields = ['prior_belief_1']
    template_name = 'tempo_mvp/prior_questions.html'


class InstructionPage(Page):
    @property
    def template_name(self):
        seq = self.session.vars['task_sequence']
        task = seq[self.round_number - 1]
        print(f"[DEBUG] Round {self.round_number}, task: {task}")
        return f'tempo_mvp/{task}/instructions.html'


class StreamingTaskPage(Page):
    """
    Switch to LivePage and the @live_method decorator so oTree
    wires up the WebSocket correctly.
    """
    form_model = 'player'
    form_fields = [
        'io_history',
        'interrupt_latency_submit',
        'interrupt_latency_stream',
    ]

    @property
    def template_name(self):
        return 'global/StreamingTask.html'

    def vars_for_template(self):
        return {'treatment': self.player.treatment}

    @staticmethod
    def live_method(self, data):
        user_input = data.get('input')
        seq = self.session.vars['task_sequence']
        idx = self.round_number - 1
        task = seq[idx] if idx < len(seq) else None
        full_output = Constants.task_texts.get(task, '')
        return {self.id_in_group: dict(output=full_output, input=user_input)}


class PostTaskSurveyPage(Page):
    form_model = 'player'

    @property
    def template_name(self):
        seq = self.session.vars['task_sequence']
        task = seq[self.round_number - 1]
        return f'tempo_mvp/{task}/post_survey.html'

    def get_form_fields(self):
        seq = self.session.vars['task_sequence']
        task = seq[self.round_number - 1]
        return [f'post_survey_rating_{task}_1']


class OverallDVPage(Page):
    form_model = 'player'
    form_fields = ['final_dv_1']
    template_name = 'tempo_mvp/post_questions.html'


page_sequence = [PriorBeliefsPage]
for _ in range(Constants.num_rounds):
    page_sequence += [InstructionPage, StreamingTaskPage, PostTaskSurveyPage]
page_sequence.append(OverallDVPage)
