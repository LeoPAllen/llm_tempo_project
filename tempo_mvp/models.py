from otree.api import *
import random, json

GLOBAL_TREAMTMENTS = [
    'slow_stream',
    'medium_stream',
    'fast_stream',
]

GLOBAL_TASK_DESCRIPTION = "Your job is to complete a task."

GLOBAL_LLM_OUTPUT = "I advise you to..."

class Constants(BaseConstants):
    name_in_url = 'tempo_mvp'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        print("DEBUG: running creating_session")
        for p in self.get_players():
            p.treatment = random.choice(GLOBAL_TREAMTMENTS)
            print(p.treatment)
            p.io_history = json.dumps([])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Assigned in creating_session
    treatment = models.StringField()

    # Prior beliefs
    prior_beliefs = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        label="How much do you like LLMs?",
        widget=widgets.RadioSelect
    )

    # pre-interaction task
    pre_interaction_task = models.IntegerField(
        min=0, 
        max=10,
        label=GLOBAL_TASK_DESCRIPTION
    )

    # JSON history of {prompt, response} tuples
    io_history = models.LongStringField()

    # post-interaction task
    post_interaction_task = models.IntegerField(
        min=0, 
        max=10,
        label=GLOBAL_TASK_DESCRIPTION
    )

    # Dependent variable 1
    perceived_accuracy = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        label="How accurate was the LLM's response?",
        widget=widgets.RadioSelect
    )

    # Dependent variable 2
    delegate_future = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        label="Would you use this assistant for future tasks?",
        widget=widgets.RadioSelect
    )
