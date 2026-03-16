from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, widgets


class Constants(BaseConstants):
    name_in_url = 'pre_tasks_measures'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


LIKERT_7 = [(i, str(i)) for i in range(1, 8)]


class Player(BasePlayer):
    page_times = models.LongStringField(blank=True)

    practice_io_history = models.LongStringField(blank=True)

    practice_attention_check = models.StringField(
        choices=[
            ('white', 'White'),
            ('grey', 'Grey'),
            ('brown', 'Brown'),
            ('green', 'Green'),
        ],
        label='Based on the LLM output, what color are arctic foxes in the winter?',
        widget=widgets.RadioSelect,
    )

    trust_automation_confident = models.IntegerField(
        choices=LIKERT_7,
        label='I am confident in advice provided by AI systems.',
        widget=widgets.RadioSelectHorizontal,
    )
    trust_automation_reliable = models.IntegerField(
        choices=LIKERT_7,
        label='AI systems are generally reliable sources of guidance.',
        widget=widgets.RadioSelectHorizontal,
    )
    trust_automation_trust = models.IntegerField(
        choices=LIKERT_7,
        label='I can trust an AI assistant to provide useful help on unfamiliar tasks.',
        widget=widgets.RadioSelectHorizontal,
    )

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

    prior_llm_accuracy = models.IntegerField(
        choices=LIKERT_7,
        label='How accurate do you believe LLMs are in general? (1 = Very inaccurate, 7 = Very accurate)',
        widget=widgets.RadioSelectHorizontal,
    )
    prior_algo_vs_human = models.IntegerField(
        choices=LIKERT_7,
        label='To what extent do you believe algorithms outperform humans in decision-making tasks? (1 = Not at all, 7 = Completely)',
        widget=widgets.RadioSelectHorizontal,
    )
    prior_llm_used_before = models.StringField(
        choices=[('yes', 'Yes'), ('no', 'No'), ('unsure', 'Not sure')],
        label='Have you used an LLM before?',
        widget=widgets.RadioSelectHorizontal,
    )
    prior_llm_judgment_conf = models.IntegerField(
        choices=LIKERT_7,
        label="How confident are you in your ability to judge whether an LLM's output is reliable? (1 = Not at all confident, 7 = Extremely confident)",
        widget=widgets.RadioSelectHorizontal,
    )
    self_rated_numeracy = models.IntegerField(
        choices=LIKERT_7,
        label='How strong do you consider your quantitative reasoning skills? (1 = Very weak, 7 = Very strong)',
        widget=widgets.RadioSelectHorizontal,
    )
    self_rated_reflection = models.IntegerField(
        choices=LIKERT_7,
        label='How likely are you to stop and rethink an initial answer before making a decision? (1 = Very unlikely, 7 = Very likely)',
        widget=widgets.RadioSelectHorizontal,
    )
