import json

from otree.api import Submission, expect

from . import pages
from ._builtin import Bot
from .models import (
    DEFAULT_TASK_IDS,
    STUDY_1_ADVICE_AMOUNTS,
    study_1_advice_text,
    get_task_definition,
    is_study_1_session,
)


def numeric_response_for_task(task_id):
    if task_id == 'time_preference':
        return 90
    return 50


def advice_timer_form_data():
    return dict(
        advice_page_loaded_at_ms=1000000,
        advice_stream_started_at_ms=1000100,
        advice_stream_ended_at_ms=1001200,
        advice_next_clicked_at_ms=1003200,
        advice_elapsed_load_to_next_ms=3200,
        advice_elapsed_stream_end_to_next_ms=2000,
    )


class PlayerBot(Bot):
    def play_round(self):
        if is_study_1_session(self.session):
            expect(self.participant.vars.get('task_order'), ['dictator'])
            expect(self.participant.vars.get('active_task_ids'), ['dictator'])
            if self.round_number > 1:
                expect(self.player.task_id, '')
                return
            expect(self.player.task_id, 'dictator')
            expect(self.player.advice_amount, 'in', STUDY_1_ADVICE_AMOUNTS)
        else:
            task_order = self.participant.vars.get('task_order')
            expect(len(task_order), len(DEFAULT_TASK_IDS))
            expect(set(task_order), set(DEFAULT_TASK_IDS))
            expect(self.player.task_id, task_order[self.round_number - 1])

        task = get_task_definition(self.player)
        if is_study_1_session(self.session):
            expect(task['llm_output'], study_1_advice_text(self.player.advice_amount))

        pre_response = numeric_response_for_task(self.player.task_id)
        post_response = pre_response

        yield pages.PreAnswerPage, dict(
            pre_numeric_response=pre_response,
            pre_confidence=4,
        )

        llm_form = dict(
            io_history=json.dumps(
                [{'input': task['llm_prompt'], 'output': task['llm_output']}]
            ),
            interrupt_latency_submit='',
            interrupt_latency_stream='',
            interrupted_stream='False',
        )
        llm_form.update(advice_timer_form_data())
        yield Submission(pages.LLMAdvicePage, llm_form)

        if is_study_1_session(self.session):
            expect(self.player.advice_page_loaded_at_ms, 1000000)
            expect(self.player.advice_stream_started_at_ms, 1000100)
            expect(self.player.advice_stream_ended_at_ms, 1001200)
            expect(self.player.advice_next_clicked_at_ms, 1003200)
            expect(self.player.advice_elapsed_load_to_next_ms, 3200)
            expect(self.player.advice_elapsed_stream_end_to_next_ms, 2000)

        yield pages.RevisedAnswerPage, dict(
            post_numeric_response=post_response,
            post_confidence=4,
        )
        mechanism_data = dict(
            confidence_in_ai=4,
        )
        if is_study_1_session(self.session):
            expect("The AI's recommendation was logical and well-reasoned.", 'not in', self.html)
            expect("I felt comfortable following the AI's recommendation.", 'not in', self.html)
            expect('I would use a similar AI again for decisions like this.', 'in', self.html)
            expect('The AI seemed to think carefully before responding.', 'in', self.html)
            expect('How much mental effort was required to understand the AI response?', 'in', self.html)
            expect('How easy was it to follow the AI response?', 'in', self.html)
            expect('How much mental fatigue did you feel after reading the AI response?', 'in', self.html)
            expect('How much effort do you think the AI exerted on your behalf?', 'in', self.html)
            expect('How much expertise do you think the AI has?', 'in', self.html)
            expect('How thorough was the AI in generating the best response for you?', 'in', self.html)
            expect('Evaluating the AI recommendation required a lot of mental effort.', 'not in', self.html)
            expect('The AI seemed to put effort into generating the recommendation.', 'not in', self.html)
            expect('TODO Study 1 cognitive tax item', 'not in', self.html)
            expect('TODO Study 1 perceived AI effort item', 'not in', self.html)
            expect('TODO Study 1 labor illusion item', 'not in', self.html)
            mechanism_data.update(
                overall_ai_future_use=4,
                overall_ai_thoughtful=4,
                cognitive_tax_mental_effort=4,
                cognitive_tax_follow_easy=4,
                cognitive_tax_mental_fatigue=4,
                labor_illusion_effort=4,
                labor_illusion_expertise=4,
                labor_illusion_thoroughness=4,
            )
        else:
            mechanism_data.update(
                cognitive_trust=4,
                affective_trust=4,
            )
        yield pages.MechanismMeasuresPage, mechanism_data
