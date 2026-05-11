from shared.timed_page import TimedPage
from tasks.models import is_study_1_session


OVERALL_AI_FIELDS = [
    'overall_ai_future_use',
    'overall_ai_thoughtful',
]

BASE_POST_SURVEY_FIELDS = [
    'trust_automation_confident',
    'trust_automation_reliable',
    'trust_automation_trust',
    'need_for_cognition_effort',
    'need_for_cognition_enjoy',
    'need_for_cognition_avoid',
    'prior_llm_used_before',
    'prior_llm_accuracy',
]


class ManipulationCheckPage(TimedPage):
    template_name = 'post_tasks_measures/ManipulationCheckPage.html'
    form_model = 'player'
    form_fields = [
        'manip_ai_responded_quickly',
        'manip_words_appeared_fast',
    ]


class PostSurveyPage(TimedPage):
    template_name = 'post_tasks_measures/PostSurveyPage.html'
    form_model = 'player'

    def get_form_fields(self):
        fields = BASE_POST_SURVEY_FIELDS[:]
        if not is_study_1_session(self.session):
            fields = OVERALL_AI_FIELDS + fields
        return fields

    def vars_for_template(self):
        return dict(is_study_1=is_study_1_session(self.session))


class DemographicsPage(TimedPage):
    template_name = 'post_tasks_measures/DemographicsPage.html'
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'education_level',
        'employment_status',
        'income_range',
    ]

    def error_message(self, values):
        age = values.get('age')
        if age is not None and not (18 <= age <= 90):
            return 'Please enter a valid age between 18 and 90.'


page_sequence = [ManipulationCheckPage, PostSurveyPage, DemographicsPage]
