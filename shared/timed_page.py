import json
from otree.api import *
from datetime import datetime


class TimedPage(Page):
    def vars_for_template(self):
        self.participant.vars['page_entry_time'] = datetime.utcnow()
        return super().vars_for_template()

    def before_next_page(self):
        start = self.participant.vars.get('page_entry_time')
        if start:
            elapsed_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
            page_times = self.participant.vars.get('page_times', {})
            page_times[self.__class__.__name__] = elapsed_ms
            self.participant.vars['page_times'] = page_times
            self.player.page_times = json.dumps(page_times)

    def is_displayed(self):
        from consent.pages import ConsentPage  # import here to avoid circular imports
        from conclusion.pages import Conclusion
        return (
            not self.participant.vars.get('consent_declined', False)
            or isinstance(self, ConsentPage)
            or isinstance(self, Conclusion)
        )