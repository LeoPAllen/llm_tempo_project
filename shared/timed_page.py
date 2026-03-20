import json
from otree.api import *
from datetime import datetime, timezone


class TimedPage(Page):
    def get_context_data(self, **kwargs):
        """Override Django's get_context_data to always record page entry time.
        This runs regardless of whether subclasses override vars_for_template."""
        self.participant.vars['page_entry_time'] = datetime.now(timezone.utc)
        return super().get_context_data(**kwargs)

    def before_next_page(self):
        start = self.participant.vars.get('page_entry_time')
        if start:
            elapsed_ms = int((datetime.now(timezone.utc) - start).total_seconds() * 1000)
            page_times = self.participant.vars.get('page_times', {})
            key = f'{self.__class__.__name__}_round_{self.round_number}'
            visibility_data = None
            if hasattr(self, 'request'):
                raw_visibility = self.request.POST.get('visibility_data')
                if raw_visibility:
                    try:
                        visibility_data = json.loads(raw_visibility)
                    except json.JSONDecodeError:
                        visibility_data = dict(parse_error=True, raw=raw_visibility)
            page_times[key] = dict(
                elapsed_ms=elapsed_ms,
                visibility=visibility_data,
            )
            self.participant.vars['page_times'] = page_times
            self.player.page_times = json.dumps(page_times)

    def is_displayed(self):
        from consent.pages import ConsentPage  # import here to avoid circular imports
        from conclusion.pages import Conclusion
        from pre_tasks_measures.pages import FailedAttentionPage
        # Always show consent, conclusion, and the failed attention page
        if isinstance(self, (ConsentPage, Conclusion, FailedAttentionPage)):
            return True
        # Block if consent declined or attention check failed
        if self.participant.vars.get('consent_declined', False):
            return False
        if self.participant.vars.get('failed_attention', False):
            return False
        return True
