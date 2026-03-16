from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, widgets


class Constants(BaseConstants):
    name_in_url = 'post_tasks_measures'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


LIKERT_7 = [(i, str(i)) for i in range(1, 8)]


class Player(BasePlayer):
    page_times = models.LongStringField(blank=True)

    overall_ai_usefulness = models.IntegerField(
        choices=LIKERT_7,
        label='Across all tasks, the AI assistant was useful.',
        widget=widgets.RadioSelectHorizontal,
    )
    overall_ai_ease_of_use = models.IntegerField(
        choices=LIKERT_7,
        label='Across all tasks, the AI assistant was easy to use.',
        widget=widgets.RadioSelectHorizontal,
    )
    overall_ai_trust = models.IntegerField(
        choices=LIKERT_7,
        label='Across all tasks, I trusted the AI assistant.',
        widget=widgets.RadioSelectHorizontal,
    )
    overall_ai_helped_quality = models.IntegerField(
        choices=LIKERT_7,
        label='Across all tasks, the AI assistant improved the quality of my decisions.',
        widget=widgets.RadioSelectHorizontal,
    )
    overall_ai_future_use = models.IntegerField(
        choices=LIKERT_7,
        label='I would use an AI assistant again for similar tasks in the future.',
        widget=widgets.RadioSelectHorizontal,
    )
    overall_ai_thoughtful = models.IntegerField(
        choices=LIKERT_7,
        label='The pace of the assistant made its responses feel thoughtful.',
        widget=widgets.RadioSelectHorizontal,
    )

    age = models.IntegerField(min=18, max=120, label='Age')
    gender = models.StringField(
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer_not', 'Prefer not to answer'),
        ],
        label='Gender',
        widget=widgets.RadioSelect,
    )
    education_level = models.StringField(
        choices=[
            ('high_school', 'High school or equivalent'),
            ('some_college', 'Some college'),
            ('bachelors', "Bachelor's degree"),
            ('masters', "Master's degree"),
            ('doctorate', 'Doctorate or professional degree'),
            ('other', 'Other'),
            ('prefer_not', 'Prefer not to answer'),
        ],
        label='Education level',
        widget=widgets.RadioSelect,
    )
    job_title = models.StringField(blank=True, label='Job')
    years_experience = models.IntegerField(blank=True, min=0, max=100, label='Years of experience')
