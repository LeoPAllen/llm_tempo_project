import json
from otree.api import *
from datetime import datetime, timezone


class TimedPage(Page):
    def _capture_prolific_id(self):
        request = getattr(self, 'request', None)
        participant_label = (getattr(self.participant, 'label', '') or '').strip()
        stored = (self.participant.vars.get('prolific_id', '') or '').strip()

        if not request:
            prolific_id = stored or participant_label
        else:
            query_params = getattr(request, 'query_params', None)
            get_params = getattr(request, 'GET', None)
            params = query_params or get_params or {}
            prolific_id = (
                params.get('PROLIFIC_PID', '')
                or params.get('prolific_pid', '')
                or params.get('participant_id', '')
                or params.get('participant_label', '')
                or stored
                or participant_label
            ).strip()

        if prolific_id:
            self.participant.vars['prolific_id'] = prolific_id
            if not participant_label:
                self.participant.label = prolific_id

    def get_context_data(self, **kwargs):
        """Override Django's get_context_data to always record page entry time.
        This runs regardless of whether subclasses override vars_for_template."""
        self._capture_prolific_id()
        self.participant.vars['page_entry_time'] = datetime.now(timezone.utc)
        return super().get_context_data(**kwargs)

    def before_next_page(self):
        start = self.participant.vars.get('page_entry_time')
        if start:
            elapsed_ms = int((datetime.now(timezone.utc) - start).total_seconds() * 1000)
            page_times = self.participant.vars.get('page_times', {})
            key = f'{self.__class__.__name__}_round_{self.round_number}'
            visibility_data = None
            if getattr(self, '_form_data', None):
                raw_visibility = self._form_data.get('visibility_data')
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
        from consent.pages import TerminationPage
        from pre_tasks_measures.pages import FailedAttentionPage
        # Always show consent and termination pages when they are the active outcome.
        if isinstance(self, (ConsentPage, TerminationPage, FailedAttentionPage)):
            return True
        if self.participant.vars.get('failed_attention', False):
            return False
        # Block if consent declined or attention check failed
        if self.participant.vars.get('consent_declined', False):
            return False
        return True
