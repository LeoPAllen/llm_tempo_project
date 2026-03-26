from otree.api import *
from .models import Constants
from shared.timed_page import TimedPage

class ConsentPage(TimedPage):
    form_model = 'player'
    form_fields = ['consent', 'prolific_id']

    @staticmethod
    def _extract_prolific_id(page):
        request = getattr(page, 'request', None)
        if not request:
            return ''
        query_params = getattr(request, 'query_params', None)
        if query_params:
            return (
                query_params.get('PROLIFIC_PID', '')
                or query_params.get('prolific_pid', '')
                or query_params.get('participant_id', '')
            )
        get_params = getattr(request, 'GET', None)
        if get_params:
            return (
                get_params.get('PROLIFIC_PID', '')
                or get_params.get('prolific_pid', '')
                or get_params.get('participant_id', '')
            )
        return ''

    def before_next_page(self):
        super().before_next_page()
        submitted_prolific_id = (self.player.prolific_id or '').strip()
        prolific_id = submitted_prolific_id or self._extract_prolific_id(self)
        self.player.prolific_id = prolific_id
        self.participant.vars['prolific_id'] = prolific_id
        if self.player.consent != 'yes':
            self.participant.vars['consent_declined'] = True
            self.participant.vars['terminated_without_pay'] = True

    def vars_for_template(self):
        return dict(
            estimated_minutes=Constants.estimated_minutes,
            contact_email=Constants.contact_email,
            prolific_id=self._extract_prolific_id(self),
        )

class TerminationPage(TimedPage):
    template_name = 'consent/FailedHumanCheckPage.html'

    def is_displayed(self):
        return self.participant.vars.get('consent_declined', False)

    def vars_for_template(self):
        return dict(
            termination_reason='You indicated that you do not consent to participate, so the study has ended.',
            payment_note='You are not eligible for payment.',
        )

page_sequence = [ConsentPage, TerminationPage]
