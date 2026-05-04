from otree.api import expect

from . import pages
from ._builtin import Bot
from tasks.models import is_study_1_session


class PlayerBot(Bot):
    def play_round(self):
        yield pages.ManipulationCheckPage, dict(
            manip_ai_responded_quickly=4,
            manip_words_appeared_fast=4,
        )

        post_survey_data = dict(
            overall_ai_future_use=4,
            overall_ai_thoughtful=4,
            trust_automation_confident=4,
            trust_automation_reliable=4,
            trust_automation_trust=4,
            need_for_cognition_effort=4,
            need_for_cognition_enjoy=4,
            need_for_cognition_avoid=4,
            prior_llm_used_before='yes',
            prior_llm_accuracy=4,
        )
        if is_study_1_session(self.session):
            expect('How much mental effort was required to understand the AI response?', 'not in', self.html)
            expect('How easy was it to follow the AI response?', 'not in', self.html)
            expect('How much mental fatigue did you feel after reading the AI response?', 'not in', self.html)
            expect('How much effort do you think the AI exerted on your behalf?', 'not in', self.html)
            expect('How much expertise do you think the AI has?', 'not in', self.html)
            expect('How thorough was the AI in generating the best response for you?', 'not in', self.html)
            expect('Evaluating the AI recommendation required a lot of mental effort.', 'not in', self.html)
            expect('The AI seemed to put effort into generating the recommendation.', 'not in', self.html)
            expect('TODO Study 1 cognitive tax item', 'not in', self.html)
            expect('TODO Study 1 perceived AI effort item', 'not in', self.html)
            expect('TODO Study 1 labor illusion item', 'not in', self.html)
            expect('labor_illusion', 'not in', self.html)
            expect('cognitive tax', 'not in', self.html)
            expect('AI effort', 'not in', self.html)
        yield pages.PostSurveyPage, post_survey_data

        yield pages.DemographicsPage, dict(
            age=30,
            gender='prefer_not',
            education_level='bachelors',
            employment_status='full_time',
            income_range='prefer_not',
        )
