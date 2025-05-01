from otree.api import *
import random, json

GLOBAL_TREAMTMENTS = [
    'default',
    'fast_start_fast_stream',
    'fast_start_slow_stream',
    'slow_start_slow_stream',
    'slow_start_fast_stream',
]


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

    # JSON history of {prompt, response} tuples
    io_history = models.LongStringField()

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
