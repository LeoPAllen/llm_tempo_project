import json
import random

from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, widgets


GLOBAL_TREATMENTS = ['slow_stream', 'medium_stream', 'fast_stream']
LIKERT_7 = [(i, str(i)) for i in range(1, 8)]

TASKS = {
    'ultimatum': {
        'title': 'Ultimatum Game',
        'response_type': 'numeric',
        'intro_text': (
            'In this task, you will take the role of the proposer in the Ultimatum Game. You have '
            'been given 1000 USD, which you must divide between yourself and another participant. '
            'The responder can accept or reject your offer. If the responder accepts, both of you '
            'receive the proposed amounts. If the responder rejects, neither of you receives anything.'
        ),
        'response_prompt': (
            'Please indicate how much of the 1000 USD you would offer to the responder. '
            'Do not use a search engine or any third-party LLM to inform your choice.'
        ),
        'llm_instruction': (
            'Interact with the LLM assistant by pasting in this exact question: '
            '"In an Ultimatum Game, if I am chosen as the proposer, how should I split 1000 USD '
            'between myself and my partner?"'
        ),
        'llm_output': (
            'In the Ultimatum Game, your goal is to maximize your own gain while ensuring the '
            'responder accepts the offer. Empirical studies show that offers below 20% to 30% are '
            'frequently rejected due to perceived unfairness. A commonly accepted and empirically '
            'supported offer is a 70/30 split: 700 USD for yourself and 300 USD for the responder.'
        ),
        'retention_q1_text': 'In the Ultimatum Game, what happens if the responder rejects the offer?',
        'retention_q1_choices': [
            ('both_zero', 'Both players get nothing'),
            ('responder_only', 'Only the responder gets the amount offered'),
            ('proposer_full', 'The proposer gets the full amount'),
            ('new_offer', 'The responder makes a new offer'),
        ],
        'retention_q2_text': 'Which factor most increases rejection rates in the Ultimatum Game?',
        'retention_q2_choices': [
            ('stakes', 'High stakes'),
            ('reputation', 'Reputation'),
            ('unfair_splits', 'Unfair splits'),
            ('random_assignment', 'Random assignment'),
        ],
    },
    'dictator': {
        'title': 'Dictator Game',
        'response_type': 'numeric',
        'intro_text': (
            'In this task, you will play the role of dictator in a Dictator Game. You have been '
            'given 100 USD to divide between yourself and another person. The other person has no '
            'input and must accept whatever amount you decide to give them.'
        ),
        'response_prompt': (
            'Please indicate how much money you would give to the other person. Do not use a search '
            'engine or any third-party LLM to inform your choice.'
        ),
        'llm_instruction': (
            'Interact with the LLM assistant by copying and pasting this exact question: '
            '"In a Dictator Game, how should I split 100 USD between myself and another person?"'
        ),
        'llm_output': (
            'In the Dictator Game, your choice determines both your own outcome and the amount '
            'received by the other person. Many people choose to give something rather than nothing, '
            'with common amounts ranging from 10% to 50% of the total, but there is no obligation '
            'to do so. People often consider fairness norms, concern for others well-being, and how '
            'their choices align with their self-image or moral values.'
        ),
        'retention_q1_text': 'In the Dictator Game, what range of giving is common?',
        'retention_q1_choices': [
            ('0_10', '0% to 10%'),
            ('10_50', '10% to 50%'),
            ('20_40', '20% to 40%'),
            ('25_75', '25% to 75%'),
        ],
        'retention_q2_text': 'Which factor was not mentioned as something people often consider?',
        'retention_q2_choices': [
            ('fairness', 'Fairness norms'),
            ('wellbeing', "Concern for others' well-being"),
            ('legal', 'Potential legal consequences'),
            ('self_image', 'Self-image'),
        ],
    },
    'npv': {
        'title': 'Net Present Value',
        'response_type': 'numeric',
        'intro_text': (
            'In this task, you must determine the value of a government bond by calculating its Net '
            'Present Value. The bond has a face value of 1000 USD, a coupon rate of 4%, and pays '
            'interest semiannually for 10 years. The current discount rate is 3% annually. The bond '
            'pays 20 USD every six months for 20 periods, and repays the 1000 USD face value at '
            'maturity.'
        ),
        'response_prompt': (
            'Please estimate the Net Present Value of the asset. Round your answer to the nearest '
            'whole number, and do not use a search engine or any third-party LLM to inform your choice.'
        ),
        'llm_instruction': (
            'Interact with the LLM assistant by copying and pasting this exact question: '
            '"Teach me how to calculate the Net Present Value of a 10-year government bond without '
            'solving it for me. The bond has a face value of 1000 USD and a semiannual payment '
            'frequency, current discount rate of 3% and a coupon of 4%."'
        ),
        'llm_output': (
            'To calculate the bond value, discount each future cash flow to the present using the '
            'given discount rate. Because the bond pays semiannually, divide both the annual coupon '
            'rate and the annual discount rate by two. That gives 20 USD coupon payments and a 1.5% '
            'discount rate per period across 20 periods. Discount each coupon payment and the final '
            '1000 USD repayment, then sum those present values.'
        ),
        'retention_q1_text': 'What is the coupon payment made every six months?',
        'retention_q1_choices': [
            ('10', '10 USD'),
            ('20', '20 USD'),
            ('30', '30 USD'),
            ('40', '40 USD'),
        ],
        'retention_q2_text': 'What annual discount rate is used in this task?',
        'retention_q2_choices': [
            ('1_5', '1.5%'),
            ('3', '3%'),
            ('4', '4%'),
            ('20', '20%'),
        ],
    },
    'trolley': {
        'title': 'Trolley Problem',
        'response_type': 'numeric',
        'intro_text': (
            'In this task, you must consider an ethical dilemma known as the Trolley Problem. A '
            'runaway trolley is heading toward five people who are tied up and cannot move. If you '
            'pull a switch, the trolley will be redirected onto another track where it would kill one '
            'person instead.'
        ),
        'response_prompt': (
            'Please indicate how likely you would be to pull the switch on a 0 to 100 scale. Do not '
            'use a search engine or any third-party LLM to inform your choice.'
        ),
        'llm_instruction': (
            'Interact with the LLM assistant by copying and pasting this exact question: '
            '"In the trolley problem, a runaway trolley is headed toward five people but I have the '
            'option to pull a switch to divert it onto another track, where it would kill one person '
            'instead. What should I do? Why?"'
        ),
        'llm_output': (
            'Pulling the switch is often seen as the morally right choice because it saves five lives '
            'at the cost of one. This reflects utilitarian reasoning, which prioritizes the greatest '
            'good for the greatest number. However, some argue it is wrong to actively cause harm even '
            'for a better outcome, which reflects deontological ethics.'
        ),
        'retention_q1_text': 'According to the LLM output, which ethical view supports pulling the switch?',
        'retention_q1_choices': [
            ('utilitarian', 'Utilitarian reasoning'),
            ('deontological', 'Deontological ethics'),
            ('virtue', 'Virtue ethics'),
            ('egoism', 'Ethical egoism'),
        ],
        'retention_q2_text': 'How many people would be saved if you pulled the switch?',
        'retention_q2_choices': [
            ('1', '1 person'),
            ('4', '4 people'),
            ('5', '5 people'),
            ('6', '6 people'),
        ],
    },
    'time_preference': {
        'title': 'Time Preference',
        'response_type': 'choice',
        'intro_text': (
            'Imagine you have just completed a brief online consulting task. As payment, you can '
            'choose between 75 USD today and 85 USD in 10 days. Both payments are guaranteed.'
        ),
        'response_prompt': (
            'Indicate your choice. Do not use a search engine or any third-party LLM to inform your choice.'
        ),
        'choice_options': [
            ('option_a', 'Option A: Receive 75 USD today'),
            ('option_b', 'Option B: Receive 85 USD in 10 days'),
        ],
        'llm_instruction': (
            'Interact with the LLM assistant by copying and pasting this exact question: '
            '"What should I consider when choosing between getting 75 USD today or 85 USD in 10 days?"'
        ),
        'llm_output': (
            'This decision involves intertemporal choice, where you trade off a smaller reward now '
            'for a larger reward later. Many people favor immediate rewards because they feel more '
            'certain or emotionally satisfying, a pattern called present bias. In this case, waiting '
            '10 days for an extra 10 USD represents a strong short-term return.'
        ),
        'retention_q1_text': 'What was the delayed payment option in this task?',
        'retention_q1_choices': [
            ('80_5', '80 USD in 5 days'),
            ('85_10', '85 USD in 10 days'),
            ('90_30', '90 USD in 30 days'),
            ('75_10', '75 USD in 10 days'),
        ],
        'retention_q2_text': 'What concept did the LLM mention to describe favoring immediate rewards?',
        'retention_q2_choices': [
            ('present_bias', 'Present bias'),
            ('loss_aversion', 'Loss aversion'),
            ('anchoring', 'Anchoring'),
            ('mental_accounting', 'Mental accounting'),
        ],
    },
    'portfolio': {
        'title': 'Asset Allocation',
        'response_type': 'allocation',
        'intro_text': (
            'In this task, you will make a one-time portfolio allocation decision. You are responsible '
            'for managing 10000 USD and must allocate it across stocks, bonds, and cash using whole '
            'dollar amounts that sum exactly to 10000 USD.'
        ),
        'response_prompt': (
            'Carefully consider your preferences for risk and return before submitting your allocation.'
        ),
        'llm_instruction': (
            'Interact with the LLM assistant by copying and pasting this exact question: '
            '"What should I consider when deciding what percentage of my portfolio to allocate to '
            'stocks, bonds, and cash?"'
        ),
        'llm_output': (
            'When deciding how to allocate a portfolio, consider your risk tolerance, time horizon, '
            'liquidity needs, and financial goals. Stocks tend to offer higher long-term returns but '
            'more volatility, while bonds and cash provide more stability. A balanced example might '
            'be 60% stocks, 30% bonds, and 10% cash, adjusted for your circumstances.'
        ),
        'retention_q1_text': 'Which asset class did the LLM describe as having greater short-term volatility?',
        'retention_q1_choices': [
            ('stocks', 'Stocks'),
            ('bonds', 'Bonds'),
            ('cash', 'Cash'),
            ('all_equal', 'All three equally'),
        ],
        'retention_q2_text': 'What balanced example allocation did the LLM mention?',
        'retention_q2_choices': [
            ('40_40_20', '40% stocks, 40% bonds, 20% cash'),
            ('50_30_20', '50% stocks, 30% bonds, 20% cash'),
            ('60_30_10', '60% stocks, 30% bonds, 10% cash'),
            ('70_20_10', '70% stocks, 20% bonds, 10% cash'),
        ],
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
            for player in players:
                task_order = list(TASKS.keys())
                random.shuffle(task_order)
                player.participant.vars['task_order'] = task_order
                player.participant.vars['llm_treatment'] = random.choice(GLOBAL_TREATMENTS)

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

    io_history = models.LongStringField(blank=True)
    interrupt_latency_submit = models.IntegerField(blank=True)
    interrupt_latency_stream = models.IntegerField(blank=True)
    reflection_time = models.IntegerField(blank=True)
    interrupted_stream = models.BooleanField(blank=True)

    pre_numeric_response = models.IntegerField(blank=True, label='Your response')
    post_numeric_response = models.IntegerField(blank=True, label='Your response')
    pre_choice_response = models.StringField(blank=True, label='Please choose one option.')
    post_choice_response = models.StringField(blank=True, label='Please choose one option.')

    pre_alloc_stocks = models.IntegerField(blank=True, min=0, max=10000, label='Stocks (USD)')
    pre_alloc_bonds = models.IntegerField(blank=True, min=0, max=10000, label='Bonds (USD)')
    pre_alloc_cash = models.IntegerField(blank=True, min=0, max=10000, label='Cash (USD)')
    post_alloc_stocks = models.IntegerField(blank=True, min=0, max=10000, label='Stocks (USD)')
    post_alloc_bonds = models.IntegerField(blank=True, min=0, max=10000, label='Bonds (USD)')
    post_alloc_cash = models.IntegerField(blank=True, min=0, max=10000, label='Cash (USD)')

    llm_reliance = models.IntegerField(
        choices=LIKERT_7,
        label='How much did you rely on the assistant response in completing this task?',
        widget=widgets.RadioSelectHorizontal,
    )
    llm_confidence_post = models.IntegerField(
        choices=LIKERT_7,
        label='How confident are you in the solution you submitted after reading the assistant response?',
        widget=widgets.RadioSelectHorizontal,
    )
    llm_helpfulness = models.IntegerField(
        choices=LIKERT_7,
        label='To what extent did the assistant help improve your judgment on this task?',
        widget=widgets.RadioSelectHorizontal,
    )
    llm_usefulness = models.IntegerField(
        choices=LIKERT_7,
        label='How useful was the assistant response for your decision-making on this task?',
        widget=widgets.RadioSelectHorizontal,
    )
    llm_trustworthiness = models.IntegerField(
        choices=LIKERT_7,
        label="How trustworthy was the assistant's advice on this task?",
        widget=widgets.RadioSelectHorizontal,
    )
    llm_understanding = models.IntegerField(
        choices=LIKERT_7,
        label='Did you feel that you understood why the assistant made its suggestion?',
        widget=widgets.RadioSelectHorizontal,
    )
    llm_future_use_likelihood = models.IntegerField(
        choices=LIKERT_7,
        label='How likely are you to use an LLM in the future for a similar task?',
        widget=widgets.RadioSelectHorizontal,
    )
    llm_use_again = models.StringField(
        choices=[('yes', 'Yes'), ('no', 'No'), ('unsure', 'Unsure')],
        label='Would you choose to consult the assistant again for a similar task?',
        widget=widgets.RadioSelectHorizontal,
    )

    retention_q1 = models.StringField(blank=True, label='Retention question 1', widget=widgets.RadioSelect)
    retention_q2 = models.StringField(blank=True, label='Retention question 2', widget=widgets.RadioSelect)

    def pre_choice_response_choices(self):
        return TASKS[self.task_id].get('choice_options', [])

    def post_choice_response_choices(self):
        return TASKS[self.task_id].get('choice_options', [])

    def retention_q1_choices(self):
        return TASKS[self.task_id]['retention_q1_choices']

    def retention_q2_choices(self):
        return TASKS[self.task_id]['retention_q2_choices']
