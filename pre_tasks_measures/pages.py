from shared.timed_page import TimedPage

from tasks.models import Constants as TaskConstants


PRACTICE_PROMPT = (
    'What is a common example of camouflage in the animal kingdom?'
)

PRACTICE_OUTPUT = (
    'Animals like the arctic fox use camouflage, such as changing fur color from white in '
    'the winter to brown in the summer, to blend into their environment.'
)


class PracticePage(TimedPage):
    form_model = 'player'
    form_fields = ['practice_io_history', 'practice_attention_check']

    def vars_for_template(self):
        return dict(
            practice_prompt=PRACTICE_PROMPT,
            llm_output=PRACTICE_OUTPUT,
        )

    def js_vars(self):
        treatment = self.participant.vars.get('llm_treatment', 'fast_stream')
        practice_stream_delay = 100 if treatment == 'fast_stream' else 350
        return dict(
            practice_output=PRACTICE_OUTPUT,
            practice_treatment=treatment,
            practice_stream_delay=practice_stream_delay,
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
    def is_displayed(self):
        return self.participant.vars.get('failed_attention', False)


class TransitionPage(TimedPage):
    def is_displayed(self):
        if self.participant.vars.get('failed_attention', False):
            return False
        return super().is_displayed()

    def vars_for_template(self):
        return dict(total_rounds=TaskConstants.num_rounds)


page_sequence = [PracticePage, FailedAttentionPage, TransitionPage]
