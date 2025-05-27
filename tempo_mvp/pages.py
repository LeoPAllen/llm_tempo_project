import json
from otree.api import *
from datetime import datetime
from .models import (
    GLOBAL_LLM_OUTPUT, 
    GLOBAL_LLM_INTERACTION_INSTRUCTIONS,
    GLOBAL_LLM_INTERACTION_ATTEMPTS
    )


class TimedPage(Page):
    def vars_for_template(self):
        self.participant.vars['page_entry_time'] = datetime.utcnow()
        return super().vars_for_template()

    def before_next_page(self):
        # Compute time spent on this page
        start = self.participant.vars.get('page_entry_time')
        if start:
            elapsed_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
            # Init timing dict on participant if needed
            page_times = self.participant.vars.get('page_times', {})
            page_times[self.__class__.__name__] = elapsed_ms
            self.participant.vars['page_times'] = page_times
            # Save to player model as JSON string
            self.player.page_times = json.dumps(page_times)


class InstructionPage(TimedPage):
    def vars_for_template(self):
        return dict(
            instructions="Your job is to follow instructions." 
        )

class PriorBeliefs(TimedPage):
    form_model = 'player'
    form_fields = ['prior_beliefs']


class PreInteractionTaskPage(TimedPage):
    form_model = 'player'
    form_fields = ['pre_interaction_task']

    def vars_for_template(self):
        return dict(
            task_description="Your job is to complete a task..."
        )


class LLMInteraction(TimedPage):
    form_model = 'player'
    form_fields = ['io_history', 'interrupt_latency_submit', 'interrupt_latency_stream', 'interrupted_stream', 'reflection_time']

    def vars_for_template(self):
        return dict(
            llm_interaction_instructions=GLOBAL_LLM_INTERACTION_INSTRUCTIONS
        )

    def js_vars(self):
        return dict(
            treatment=self.player.treatment,
            llm_interaction_attempts=GLOBAL_LLM_INTERACTION_ATTEMPTS  # or dynamically set
        )

    def live_method(self, data):
        user_input = data.get('input')
        # this could be replaced with an LLM call
        output = GLOBAL_LLM_OUTPUT
        return {self.id_in_group: dict(output=output, input=user_input)}

class PostInteractionTaskPage(TimedPage):
    form_model = 'player'
    form_fields = ['post_interaction_task']

    def vars_for_template(self):
        return dict(
            task_description="Your job is to complete a task..."
        )

class DVQuestions(TimedPage):
    form_model = 'player'
    form_fields = ['perceived_accuracy', 'delegate_future']


class Conclusion(TimedPage):
     def vars_for_template(self):
        return dict(
            conclusion="Thank you for participating" 
        )   

page_sequence = [
    InstructionPage, 
    PriorBeliefs, 
    PreInteractionTaskPage,
    LLMInteraction, 
    PostInteractionTaskPage,
    DVQuestions,
    Conclusion
]
