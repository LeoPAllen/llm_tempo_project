from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


doc = """s
Consent app
"""

class Constants(BaseConstants):
    name_in_url = 'consent'
    players_per_group = None
    num_rounds = 1
    contact_email = 'leo.allen@hec.edu'
    estimated_minutes = 25

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    consent = models.StringField(
        choices=[['yes', 'I consent to participate'], ['no', 'I do not consent']],
        label='Do you agree to participate in this study?',
        widget=widgets.RadioSelect,
    )
    prolific_id = models.StringField(
        blank=True,
    )
    page_times = models.LongStringField(blank=True)
