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

    # Manipulation check — perceived speed
    manip_ai_responded_quickly = models.IntegerField(
        choices=LIKERT_7,
        label='The AI responded quickly to my questions.',
        widget=widgets.RadioSelectHorizontal,
    )
    manip_waited_long = models.IntegerField(
        choices=LIKERT_7,
        label='I had to wait a long time before the AI started responding.',
        widget=widgets.RadioSelectHorizontal,
    )
    manip_words_appeared_fast = models.IntegerField(
        choices=LIKERT_7,
        label="The AI's words appeared on screen at a fast pace.",
        widget=widgets.RadioSelectHorizontal,
    )

    # Overall AI experience in this study
    overall_ai_future_use = models.IntegerField(
        choices=LIKERT_7,
        label='I would use a similar AI again for tasks like these.',
        widget=widgets.RadioSelectHorizontal,
    )
    overall_ai_thoughtful = models.IntegerField(
        choices=LIKERT_7,
        label='The AI seemed to think carefully before responding.',
        widget=widgets.RadioSelectHorizontal,
    )

    # General trust in AI (control/moderator)
    trust_automation_confident = models.IntegerField(
        choices=LIKERT_7,
        label='In general, I am confident in advice provided by AI.',
        widget=widgets.RadioSelectHorizontal,
    )
    trust_automation_reliable = models.IntegerField(
        choices=LIKERT_7,
        label='In general, AI is a reliable source of guidance.',
        widget=widgets.RadioSelectHorizontal,
    )
    trust_automation_trust = models.IntegerField(
        choices=LIKERT_7,
        label='In general, I can trust AI to provide useful help on unfamiliar tasks.',
        widget=widgets.RadioSelectHorizontal,
    )

    # Need for cognition (control/moderator)
    need_for_cognition_effort = models.IntegerField(
        choices=LIKERT_7,
        label='I prefer complex problems to simple ones.',
        widget=widgets.RadioSelectHorizontal,
    )
    need_for_cognition_enjoy = models.IntegerField(
        choices=LIKERT_7,
        label='I enjoy tasks that require a lot of thinking.',
        widget=widgets.RadioSelectHorizontal,
    )
    need_for_cognition_avoid = models.IntegerField(
        choices=LIKERT_7,
        label='I only think as hard as I have to.',
        widget=widgets.RadioSelectHorizontal,
    )

    # Prior AI experience (control)
    prior_llm_used_before = models.StringField(
        choices=[('yes', 'Yes'), ('no', 'No'), ('unsure', 'Not sure')],
        label='Have you used an AI chatbot (e.g., ChatGPT, Gemini, Claude) before?',
        widget=widgets.RadioSelectHorizontal,
    )
    prior_llm_accuracy = models.IntegerField(
        choices=LIKERT_7,
        label='How accurate do you believe AI chatbots are in general?',
        widget=widgets.RadioSelectHorizontal,
    )

    # Demographics
    age = models.IntegerField(min=18, max=90, label='Age')
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
        ],
        label='Education level',
        widget=widgets.RadioSelect,
    )
    employment_status = models.StringField(
        choices=[
            ('full_time', 'Employed full-time'),
            ('part_time', 'Employed part-time'),
            ('self_employed', 'Self-employed'),
            ('student', 'Student'),
            ('unemployed', 'Unemployed'),
            ('retired', 'Retired'),
            ('prefer_not', 'Prefer not to answer'),
        ],
        label='Employment status',
        widget=widgets.RadioSelect,
    )
    income_range = models.StringField(
        choices=[
            ('under_25k', 'Under $25,000'),
            ('25k_50k', '$25,000 – $49,999'),
            ('50k_75k', '$50,000 – $74,999'),
            ('75k_100k', '$75,000 – $99,999'),
            ('100k_150k', '$100,000 – $149,999'),
            ('over_150k', '$150,000 or more'),
            ('prefer_not', 'Prefer not to answer'),
        ],
        label='Annual household income',
        widget=widgets.RadioSelect,
    )
