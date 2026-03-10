from otree.api import *
from .models import Constants
from shared.timed_page import TimedPage

class ConsentPage(TimedPage):
    form_model = 'player'
    form_fields = ['consent']

    def before_next_page(self):
        if self.player.consent != 'yes':
            self.participant.vars['consent_declined'] = True

    def vars_for_template(self):
        return dict(
            estimated_minutes=Constants.estimated_minutes,
            contact_email=Constants.contact_email
        )

page_sequence = [ConsentPage]
