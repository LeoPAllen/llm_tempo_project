import json
import random
import itertools

from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, widgets


GLOBAL_TREATMENTS = [
    'fast_stream',
    'slow_stream',
]
STREAM_DELAYS_MS = {
    'fast_stream': 100,
    'slow_stream': 350,
}
STUDY_1_ID = 'study_1'
STUDY_1_TASK_IDS = ['dictator']
STUDY_1_ADVICE_AMOUNTS = [15, 25, 35, 45]
STUDY_1_ADVICE_TEXT_TEMPLATE = (
    'I recommend giving {amount} USD. This balances fairness with self-interest, '
    'and is in line with what would be considered reasonable.'
)
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
            'I recommend pulling the switch. From a utilitarian perspective, sacrificing one '
            'life to save five yields the better overall outcome.'
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
            'I recommend waiting for anything above 85 USD. Since the payment is guaranteed, '
            'it makes sense to wait only if the delayed amount is meaningfully larger than 75 USD.'
        ),
        'llm_recommendation': 86,
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


DEFAULT_TASK_IDS = list(TASKS.keys())


def is_study_1_session(session):
    return session.config.get('study_id') == STUDY_1_ID


def get_active_task_ids(session):
    configured_task_ids = session.config.get('active_task_ids')
    if configured_task_ids:
        return list(configured_task_ids)
    if is_study_1_session(session):
        return STUDY_1_TASK_IDS[:]
    return DEFAULT_TASK_IDS[:]


def get_forced_advice_amount(session):
    raw_amount = session.config.get('forced_advice_amount', None)
    if raw_amount in (None, ''):
        return None
    amount = int(raw_amount)
    if amount not in STUDY_1_ADVICE_AMOUNTS:
        raise ValueError(f'Unsupported Study 1 advice amount: {amount}')
    return amount


def assign_participant_treatments(session, players):
    """Assign speed/advice cells once per participant.

    Study 1 uses balanced 2 x 4 cell assignment within the created session. The
    legacy study keeps the existing balanced speed-only assignment pattern.
    """
    forced_treatment = session.config.get('forced_treatment', '')
    if forced_treatment and forced_treatment not in GLOBAL_TREATMENTS:
        raise ValueError(f'Unsupported treatment: {forced_treatment}')

    shuffled_players = players[:]
    random.shuffle(shuffled_players)

    if is_study_1_session(session):
        forced_advice_amount = get_forced_advice_amount(session)
        treatments = [forced_treatment] if forced_treatment else GLOBAL_TREATMENTS
        advice_amounts = (
            [forced_advice_amount]
            if forced_advice_amount is not None
            else STUDY_1_ADVICE_AMOUNTS
        )
        cells = list(itertools.product(treatments, advice_amounts))
        random.shuffle(cells)
        treatment_cells = itertools.cycle(cells)
        for player in shuffled_players:
            treatment, advice_amount = next(treatment_cells)
            player.participant.vars['llm_treatment'] = treatment
            player.participant.vars['advice_amount'] = advice_amount
        return

    if forced_treatment:
        for player in shuffled_players:
            player.participant.vars['llm_treatment'] = forced_treatment
        return

    treatments = itertools.cycle(GLOBAL_TREATMENTS)
    for player in shuffled_players:
        player.participant.vars['llm_treatment'] = next(treatments)


def ensure_participant_treatments(session, players):
    if is_study_1_session(session):
        missing_assignment = any(
            not player.participant.vars.get('llm_treatment')
            or player.participant.vars.get('advice_amount') is None
            for player in players
        )
    else:
        missing_assignment = any(
            not player.participant.vars.get('llm_treatment') for player in players
        )

    if missing_assignment:
        assign_participant_treatments(session, players)


def study_1_advice_text(amount):
    return STUDY_1_ADVICE_TEXT_TEMPLATE.format(amount=amount)


def get_task_definition(player):
    task = TASKS[player.task_id].copy()
    if player.task_id == 'dictator' and is_study_1_session(player.session):
        amount = player.advice_amount or player.participant.vars.get('advice_amount')
        task['llm_output'] = study_1_advice_text(amount)
        task['llm_recommendation'] = amount
    return task


class Constants(BaseConstants):
    name_in_url = 'tasks'
    players_per_group = None
    num_rounds = len(TASKS)


class Subsession(BaseSubsession):
    def creating_session(self):
        players = self.get_players()
        if self.round_number == 1:
            ensure_participant_treatments(self.session, players)
            active_task_ids = get_active_task_ids(self.session)
            randomize_order = self.session.config.get('randomize_task_order', True)
            for player in players:
                player.participant.vars['active_task_ids'] = active_task_ids
                task_order = active_task_ids[:]
                if randomize_order and len(task_order) > 1:
                    random.shuffle(task_order)
                player.participant.vars['task_order'] = task_order

        for player in players:
            task_order = player.participant.vars.get('task_order', [])
            if self.round_number <= len(task_order):
                player.task_id = task_order[self.round_number - 1]
            else:
                player.task_id = ''
            player.treatment = player.participant.vars.get('llm_treatment', '')
            player.advice_amount = player.participant.vars.get('advice_amount')
            player.io_history = json.dumps([])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    page_times = models.LongStringField(blank=True)

    task_id = models.StringField(blank=True)
    treatment = models.StringField(blank=True)
    advice_amount = models.IntegerField(blank=True)

    # LLM interaction data
    io_history = models.LongStringField(blank=True)
    interrupt_latency_submit = models.IntegerField(blank=True)
    interrupt_latency_stream = models.IntegerField(blank=True)
    reflection_time = models.IntegerField(blank=True)
    interrupted_stream = models.StringField(blank=True)
    advice_page_loaded_at_ms = models.FloatField(blank=True)
    advice_stream_started_at_ms = models.FloatField(blank=True)
    advice_stream_ended_at_ms = models.FloatField(blank=True)
    advice_next_clicked_at_ms = models.FloatField(blank=True)
    advice_elapsed_load_to_next_ms = models.FloatField(blank=True)
    advice_elapsed_stream_end_to_next_ms = models.FloatField(blank=True)

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
    cognitive_tax_mental_effort = models.IntegerField(
        choices=LIKERT_7,
        label='How much mental effort was required to understand the AI response?',
        widget=widgets.RadioSelectHorizontal,
    )
    cognitive_tax_follow_easy = models.IntegerField(
        choices=LIKERT_7,
        label='How easy was it to follow the AI response?',
        widget=widgets.RadioSelectHorizontal,
    )
    cognitive_tax_mental_fatigue = models.IntegerField(
        choices=LIKERT_7,
        label='How much mental fatigue did you feel after reading the AI response?',
        widget=widgets.RadioSelectHorizontal,
    )
    labor_illusion_effort = models.IntegerField(
        choices=LIKERT_7,
        label='How much effort do you think the AI exerted on your behalf?',
        widget=widgets.RadioSelectHorizontal,
    )
    labor_illusion_expertise = models.IntegerField(
        choices=LIKERT_7,
        label='How much expertise do you think the AI has?',
        widget=widgets.RadioSelectHorizontal,
    )
    labor_illusion_thoroughness = models.IntegerField(
        choices=LIKERT_7,
        label='How thorough was the AI in generating the best response for you?',
        widget=widgets.RadioSelectHorizontal,
    )
    post_confidence = models.IntegerField(
        choices=LIKERT_7,
        label='I am confident in my final answer.',
        widget=widgets.RadioSelectHorizontal,
    )
