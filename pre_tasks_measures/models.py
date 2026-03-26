import itertools
import random

from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, widgets

from tasks.models import GLOBAL_TREATMENTS


class Constants(BaseConstants):
    name_in_url = 'pre_tasks_measures'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        forced = self.session.config.get('forced_treatment', '')
        if forced:
            for player in self.get_players():
                player.participant.vars['llm_treatment'] = forced
            return

        players = self.get_players()
        shuffled_players = players[:]
        random.shuffle(shuffled_players)
        treatments = itertools.cycle(GLOBAL_TREATMENTS)
        for player in shuffled_players:
            player.participant.vars['llm_treatment'] = next(treatments)


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
        label='Based on the AI response above, what color are arctic foxes in the winter? However, please select "green" below.',
        widget=widgets.RadioSelect,
    )
