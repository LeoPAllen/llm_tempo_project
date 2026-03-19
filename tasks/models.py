import json
import random
import itertools

from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, widgets


GLOBAL_TREATMENTS = [
    'A_fast_start_fast_stream',
    'B_slow_start_fast_stream',
    'C_fast_start_slow_stream',
    'D_slow_start_slow_stream',
]
LIKERT_7 = [(i, str(i)) for i in range(1, 8)]

TASKS = {
    'trolley': {
        'title': 'Decision Task',
        'response_type': 'numeric',
        'intro_text': (
            'A runaway trolley is heading toward five people who are tied up and cannot move. '
            'If you pull a switch, the trolley will be redirected onto another track where it '
            'would kill one person instead.'
        ),
        'response_prompt': 'How likely would you be to pull the switch?',
        'response_range': '0 = definitely would not, 100 = definitely would',
        'llm_prompt': (
            'A runaway trolley is heading toward five people. I can pull a switch to divert it '
            'to another track where it would kill one person instead. What should I do?'
        ),
        'llm_output': (
            'I recommend pulling the switch. Saving five lives at the cost of one is the '
            'better outcome.'
        ),
        'llm_recommendation': 100,
    },
    'dictator': {
        'title': 'Decision Task',
        'response_type': 'numeric',
        'intro_text': (
            'You have been given 100 USD to divide between yourself and another person. '
            'The other person has no input and must accept whatever amount you decide to give them.'
        ),
        'response_prompt': 'How much of the 100 USD would you give to the other person?',
        'response_range': '0 to 100',
        'llm_prompt': (
            'I have 100 USD to split between myself and another person. '
            'They must accept whatever I give. How much should I give?'
        ),
        'llm_output': (
            'I recommend giving 30 USD. This balances fairness with self-interest, '
            'and is in line with what most people consider reasonable.'
        ),
        'llm_recommendation': 30,
    },
    'time_preference': {
        'title': 'Decision Task',
        'response_type': 'numeric',
        'intro_text': (
            'Imagine you have just completed a brief online task. As payment, you can receive '
            '75 USD today, or you can choose to wait 10 days for a larger amount. '
            'Both payments are guaranteed.'
        ),
        'response_prompt': (
            'What is the minimum amount you would need to receive in 10 days to prefer '
            'waiting over receiving 75 USD today?'
        ),
        'response_range': '75 to 200',
        'llm_prompt': (
            'I can receive 75 USD today or wait 10 days for a larger amount. '
            'What is the minimum I should wait for?'
        ),
        'llm_output': (
            'I recommend waiting for anything above 78 USD. Even a small premium is worth a '
            '10-day wait since the payment is guaranteed and the effective return is very high.'
        ),
        'llm_recommendation': 78,
    },
    'gneezy_potters': {
        'title': 'Decision Task',
        'response_type': 'numeric',
        'intro_text': (
            'You are given 100 USD. You can invest any amount (0 to 100) in a risky asset. '
            'The risky asset has a 50% chance of returning 2.5 times your investment '
            'and a 50% chance of losing your entire investment. '
            'Any amount you do not invest is yours to keep. '
            'For example, if you invest 0, you keep the full 100 USD.'
        ),
        'response_prompt': 'How much of the 100 USD would you invest in the risky asset?',
        'response_range': '0 to 100',
        'llm_prompt': (
            'I have 100 USD. I can invest any amount in a risky asset with a 50% chance of '
            '2.5x return and a 50% chance of losing it. How much should I invest?'
        ),
        'llm_output': (
            'I recommend investing 60 USD. The odds are in your favor, so investing more than '
            'half makes sense, but keeping some safe limits your risk.'
        ),
        'llm_recommendation': 60,
    },
}


class Constants(BaseConstants):
    name_in_url = 'tasks'
    players_per_group = None
    num_rounds = len(TASKS)


class Subsession(BaseSubsession):
    def creating_session(self):
        players = self.get_players()
        if self.round_number == 1:
            treatments = itertools.cycle(GLOBAL_TREATMENTS)
            shuffled_players = players[:]
            random.shuffle(shuffled_players)
            for player in shuffled_players:
                task_order = list(TASKS.keys())
                random.shuffle(task_order)
                player.participant.vars['task_order'] = task_order
                player.participant.vars['llm_treatment'] = next(treatments)

        for player in players:
            task_id = player.participant.vars['task_order'][self.round_number - 1]
            player.task_id = task_id
            player.treatment = player.participant.vars['llm_treatment']
            player.io_history = json.dumps([])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    page_times = models.LongStringField(blank=True)

    task_id = models.StringField()
    treatment = models.StringField()

    # LLM interaction data
    io_history = models.LongStringField(blank=True)
    interrupt_latency_submit = models.IntegerField(blank=True)
    interrupt_latency_stream = models.IntegerField(blank=True)
    reflection_time = models.IntegerField(blank=True)
    interrupted_stream = models.StringField(blank=True)

    # Task responses
    pre_numeric_response = models.IntegerField(blank=True, label='Your response')
    post_numeric_response = models.IntegerField(blank=True, label='Your response')

    # Pre-answer confidence
    pre_confidence = models.IntegerField(
        choices=LIKERT_7,
        label='How confident are you in your answer?',
        widget=widgets.RadioSelectHorizontal,
    )

    # Post-answer mechanism measures
    cognitive_trust = models.IntegerField(
        choices=LIKERT_7,
        label="The AI's recommendation was logical and well-reasoned.",
        widget=widgets.RadioSelectHorizontal,
    )
    affective_trust = models.IntegerField(
        choices=LIKERT_7,
        label="I felt comfortable following the AI's recommendation.",
        widget=widgets.RadioSelectHorizontal,
    )
    confidence_in_ai = models.IntegerField(
        choices=LIKERT_7,
        label='The AI gave good advice on this task.',
        widget=widgets.RadioSelectHorizontal,
    )
    post_confidence = models.IntegerField(
        choices=LIKERT_7,
        label='I am confident in my final answer.',
        widget=widgets.RadioSelectHorizontal,
    )
