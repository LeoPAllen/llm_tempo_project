from otree.api import expect

from . import pages
from ._builtin import Bot
from tasks.models import is_study_1_session


class PlayerBot(Bot):
    def play_round(self):
        if is_study_1_session(self.session):
            expect('4 minutes', 'in', self.html)
        else:
            expect('8 minutes', 'in', self.html)
        yield pages.ConsentPage, dict(consent='yes', prolific_id='TEST_PID')
        expect(self.participant.vars.get('prolific_id'), 'TEST_PID')
        expect(self.participant.vars.get('consent_declined', False), False)
