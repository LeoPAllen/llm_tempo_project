from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, widgets


class Constants(BaseConstants):
    name_in_url = 'pre_tasks_measures'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


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
        label="Based on the AI's response, what color are arctic foxes in the winter?",
        widget=widgets.RadioSelect,
    )
