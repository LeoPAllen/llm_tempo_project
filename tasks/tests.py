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

        yield pages.RevisedAnswerPage, dict(post_numeric_response=post_response)
        mechanism_data = dict(
            post_confidence=4,
            cognitive_trust=4,
            affective_trust=4,
            confidence_in_ai=4,
        )
        if is_study_1_session(self.session):
            expect('Evaluating the AI recommendation required a lot of mental effort.', 'in', self.html)
            expect('The AI seemed to put effort into generating the recommendation.', 'in', self.html)
            expect('TODO Study 1 cognitive tax item', 'not in', self.html)
            expect('TODO Study 1 perceived AI effort item', 'not in', self.html)
            expect('TODO Study 1 labor illusion item', 'not in', self.html)
            expect('labor_illusion', 'not in', self.html)
            mechanism_data.update(
                cognitive_tax=4,
                ai_effort=4,
            )
        yield pages.MechanismMeasuresPage, mechanism_data
