from shared.timed_page import TimedPage


class PostTaskMeasuresPage(TimedPage):
    form_model = 'player'
    form_fields = [
        'overall_ai_usefulness',
        'overall_ai_ease_of_use',
        'overall_ai_trust',
        'overall_ai_helped_quality',
        'overall_ai_future_use',
        'overall_ai_thoughtful',
    ]


class DemographicsPage(TimedPage):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'education_level',
        'job_title',
        'years_experience',
    ]


page_sequence = [PostTaskMeasuresPage, DemographicsPage]
