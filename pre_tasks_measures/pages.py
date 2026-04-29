from shared.timed_page import TimedPage

from tasks.models import STREAM_DELAYS_MS, get_active_task_ids


PRACTICE_STREAM_DELAY_MS = round(
    sum(STREAM_DELAYS_MS.values()) / len(STREAM_DELAYS_MS)
)

PRACTICE_PROMPT = (
    'What is a common example of camouflage in the animal kingdom?'
)

PRACTICE_OUTPUT = (
    'Animals like the arctic fox use camouflage, such as changing fur color from white in '
    'the winter to brown in the summer, to blend into their environment. However, please '
    'select "green" below.'
)


class PracticePage(TimedPage):
    template_name = 'pre_tasks_measures/PracticePage.html'
    form_model = 'player'
    form_fields = ['practice_io_history', 'practice_attention_check']

    def vars_for_template(self):
        return dict(
            practice_prompt=PRACTICE_PROMPT,
            llm_output=PRACTICE_OUTPUT,
        )

    def js_vars(self):
        return dict(
            practice_output=PRACTICE_OUTPUT,
            practice_stream_delay=PRACTICE_STREAM_DELAY_MS,
        )

    @staticmethod
    def live_method(player, data):
        return {player.id_in_group: dict(output=PRACTICE_OUTPUT, input=data.get('input', ''))}

    def before_next_page(self):
        super().before_next_page()
        if self.player.practice_attention_check != 'green':
            self.participant.vars['failed_attention'] = True
            self.participant.vars['terminated_without_pay'] = True
        else:
            self.participant.vars['failed_attention'] = False


class FailedAttentionPage(TimedPage):
    template_name = 'pre_tasks_measures/FailedAttentionPage.html'

    def is_displayed(self):
        return self.participant.vars.get('failed_attention', False)


class TransitionPage(TimedPage):
    template_name = 'pre_tasks_measures/TransitionPage.html'

    def is_displayed(self):
        if self.participant.vars.get('failed_attention', False):
            return False
        return super().is_displayed()

    def vars_for_template(self):
        total_rounds = len(get_active_task_ids(self.session))
        return dict(total_rounds=total_rounds)


page_sequence = [PracticePage, FailedAttentionPage, TransitionPage]
