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
        start = self.participant.vars.get('page_entry_time')
        if start:
            elapsed_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
            page_times = self.participant.vars.get('page_times', {})
            page_times[self.__class__.__name__] = elapsed_ms
            self.participant.vars['page_times'] = page_times
            self.player.page_times = json.dumps(page_times)


class InstructionPage(TimedPage):
    def vars_for_template(self):
        return dict(
            instructions="Your job is to follow instructions."
        )


class PriorBeliefs(TimedPage):
    form_model = 'player'
    form_fields = [
        'prior_llm_trust',
        'prior_llm_accuracy',
        'prior_algo_vs_human',
        'prior_llm_used_before',
        'prior_llm_judgment_conf'
    ]


class PreInteractionTaskPage(TimedPage):
    form_model = 'player'
    form_fields = ['pre_interaction_task']

    def vars_for_template(self):
        return dict(
            task_description="Your job is to complete a task..."
        )


class LLMInteraction(TimedPage):
    form_model = 'player'
    form_fields = [
        'io_history',
        'interrupt_latency_submit',
        'interrupt_latency_stream',
        'interrupted_stream',
        'reflection_time'
    ]

    def vars_for_template(self):
        return dict(
            llm_interaction_instructions=GLOBAL_LLM_INTERACTION_INSTRUCTIONS
        )

    def js_vars(self):
        return dict(
            treatment=self.player.treatment,
            llm_interaction_attempts=GLOBAL_LLM_INTERACTION_ATTEMPTS
        )

    def live_method(self, data):
        user_input = data.get('input')
        output = GLOBAL_LLM_OUTPUT
        return {self.id_in_group: dict(output=output, input=user_input)}


class PostInteractionTaskPage(TimedPage):
    form_model = 'player'
    form_fields = ['post_interaction_task']

    def vars_for_template(self):
        return dict(
            task_description="Your job is to complete a task..."
        )


class LLMAppreciationPage(TimedPage):
    form_model = 'player'
    form_fields = [
        'llm_reliance',
        'llm_confidence_post',
        'llm_helpfulness',
        'llm_future_use_likelihood',
        'llm_use_again',
    ]


class FairnessPage(TimedPage):
    form_model = 'player'
    form_fields = [
        'llm_fairness',
        'llm_objectivity',
        'llm_understanding',
        'llm_decision_fairness',
    ]


class RetentionQuizPage(TimedPage):
    form_model = 'player'
    form_fields = [
        'retention_q1',
        'retention_q2',
        'retention_q3',
    ]


class TrustUsefulnessPage(TimedPage):
    form_model = 'player'
    form_fields = [
        'llm_usefulness',
        'llm_trustworthiness',
        'llm_confidence_boost',
    ]



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
    LLMAppreciationPage,
    FairnessPage,
    RetentionQuizPage,
    TrustUsefulnessPage,
    Conclusion
]
