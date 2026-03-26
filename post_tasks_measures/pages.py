from shared.timed_page import TimedPage


class ManipulationCheckPage(TimedPage):
    form_model = 'player'
    form_fields = [
        'manip_ai_responded_quickly',
        'manip_words_appeared_fast',
    ]


class PostSurveyPage(TimedPage):
    form_model = 'player'
    form_fields = [
        'overall_ai_future_use',
        'overall_ai_thoughtful',
        'trust_automation_confident',
        'trust_automation_reliable',
        'trust_automation_trust',
        'need_for_cognition_effort',
        'need_for_cognition_enjoy',
        'need_for_cognition_avoid',
        'prior_llm_used_before',
        'prior_llm_accuracy',
    ]


class DemographicsPage(TimedPage):
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
