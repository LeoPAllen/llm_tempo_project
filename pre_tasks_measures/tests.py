import itertools

from otree.api import expect

from . import pages
from ._builtin import Bot
from tasks.models import (
    GLOBAL_TREATMENTS,
    STUDY_1_ADVICE_AMOUNTS,
    get_forced_advice_amount,
    is_study_1_session,
)


def call_live_method(method, page_class, **kwargs):
    if page_class is pages.PracticePage:
        response = method(1, dict(input=pages.PRACTICE_PROMPT))
        output = response[1]['output']
        expect(output, pages.PRACTICE_OUTPUT)
        expect('select "green" below', 'in', output)


class PlayerBot(Bot):
    def play_round(self):
        treatment = self.participant.vars.get('llm_treatment')
        expect(treatment, 'in', GLOBAL_TREATMENTS)

        if is_study_1_session(self.session):
            advice_amount = self.participant.vars.get('advice_amount')
            expect(advice_amount, 'in', STUDY_1_ADVICE_AMOUNTS)

            forced_treatment = self.session.config.get('forced_treatment')
            if forced_treatment:
                expect(treatment, forced_treatment)

            forced_advice_amount = get_forced_advice_amount(self.session)
            if forced_advice_amount is not None:
                expect(advice_amount, forced_advice_amount)

            if (
                self.player.id_in_subsession == 1
                and not forced_treatment
                and forced_advice_amount is None
                and len(self.subsession.get_players()) == 8
            ):
                observed_cells = sorted(
                    (
                        player.participant.vars.get('llm_treatment'),
                        player.participant.vars.get('advice_amount'),
                    )
                    for player in self.subsession.get_players()
                )
                expected_cells = sorted(
                    itertools.product(GLOBAL_TREATMENTS, STUDY_1_ADVICE_AMOUNTS)
                )
                expect(observed_cells, expected_cells)

        expect('To confirm you are paying attention, please select Green.', 'in', self.html)
        expect('arctic fox use camouflage', 'in', self.html)
        expect("Based on the AI's response", 'not in', self.html)
        yield pages.PracticePage, dict(
            practice_io_history='[]',
            practice_attention_check='green',
        )

        if is_study_1_session(self.session):
            expect('1 decision-making task', 'in', self.html)
        else:
            expect('4 decision-making tasks', 'in', self.html)
        yield pages.TransitionPage
