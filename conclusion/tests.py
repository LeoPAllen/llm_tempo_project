from otree.api import Submission, expect

from . import pages
from ._builtin import Bot
from tasks.models import is_study_1_session


class PlayerBot(Bot):
    def play_round(self):
        if is_study_1_session(self.session):
            expect('TODO_STUDY_1_PROLIFIC_COMPLETION_URL', 'in', self.html)
        yield Submission(pages.Conclusion, check_html=False)
