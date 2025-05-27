from otree.api import *
from .models import (GLOBAL_LLM_OUTPUT, GLOBAL_LLM_INTERACTION_INSTRUCTIONS)
import random

class InstructionPage(Page):
    def vars_for_template(self):
        return dict(
            instructions="Your job is to follow instructions." 
        )

class PriorBeliefs(Page):
    form_model = 'player'
    form_fields = ['prior_beliefs']


class PreInteractionTaskPage(Page):
    form_model = 'player'
    form_fields = ['pre_interaction_task']

    def vars_for_template(self):
        return dict(
            task_description="Your job is to complete a task..."
        )


class LLMInteraction(Page):
    form_model = 'player'
    form_fields = ['io_history', 'interrupt_latency_submit', 'interrupt_latency_stream', 'interrupted_stream']

    def vars_for_template(self):
        return dict(
            llm_interaction_instructions=GLOBAL_LLM_INTERACTION_INSTRUCTIONS
        )
    def js_vars(self):
        return dict(
            treatment=self.player.treatment # Force inject to test
        )

    def live_method(self, data):
        user_input = data.get('input')
        # this could be replaced with an LLM call
        output = GLOBAL_LLM_OUTPUT
        return {self.id_in_group: dict(output=output, input=user_input)}

class PostInteractionTaskPage(Page):
    form_model = 'player'
    form_fields = ['post_interaction_task']

    def vars_for_template(self):
        return dict(
            task_description="Your job is to complete a task..."
        )

class DVQuestions(Page):
    form_model = 'player'
    form_fields = ['perceived_accuracy', 'delegate_future']


class Conclusion(Page):
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
