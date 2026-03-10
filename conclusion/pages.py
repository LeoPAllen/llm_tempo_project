from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from shared.timed_page import TimedPage

class Conclusion(TimedPage):
    def vars_for_template(self):
        return dict(
            conclusion="Thank you for participating"
        )


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Conclusion]
