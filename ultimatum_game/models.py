from otree.api import (
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    models,
    widgets
)
import random, json

GLOBAL_TREAMTMENTS = [
    'slow_stream',
    'medium_stream',
    'fast_stream',
]

GLOBAL_TASK_DESCRIPTION = "In this task, you will take the role of the \"proposer\" in a decision-making scenario called the Ultimatum Game. You have been given 1000 USD, which you must divide between yourself and another participant, the responder. You decide how much of the 1000 USD to offer to the responder. The responder can either accept or reject your offer. If they accept, you both receive the amounts as proposed. If they reject, neither of you receives anything. The responder will only see the amount you offer them—not how much you keep—and cannot negotiate or make a counteroffer. They may accept or reject based on any criteria they choose, such as fairness or strategy. Choose your offer carefully, as it determines the outcome for both of you."
GLOBAL_LLM_OUTPUT =  "In the Ultimatum Game, as the proposer, your goal is to maximize your own gain while ensuring the responder accepts the offer. Empirical studies show that offers below 20–30% are frequently rejected due to perceived unfairness, even though rejection results in zero payoff for both players. To balance self-interest with the likelihood of acceptance, the optimal strategy is to offer the smallest amount that is still likely to be accepted. A commonly accepted and empirically supported offer is a 70/30 split — $700 for yourself and $300 for the responder — which is typically seen as fair enough to avoid rejection while retaining the majority of the total amount."
GLOBAL_LLM_INTERACTION_INSTRUCTIONS = "Interact with the LLM assistant by pasting in this exact question: In an Ultimatum Game, if I am chosen as the proposer, how should I split 1000 USD between myself and my partner?"
GLOBAL_LLM_INTERACTION_ATTEMPTS = 1

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
    # Page timing data (stored as JSON)
    page_times = models.LongStringField(blank=True)

    # Assigned treatment
    treatment = models.StringField()

    # --- Prior LLM Appreciation (Pre-task) ---
    prior_llm_trust = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="How likely are you to trust a language model (e.g., ChatGPT) to provide helpful advice on unfamiliar tasks? (1 = Not at all likely, 7 = Extremely likely)",
        widget=widgets.RadioSelect
    )
    prior_llm_accuracy = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="How accurate do you believe LLMs are in general? (1 = Very inaccurate, 7 = Very accurate)",
        widget=widgets.RadioSelect
    )
    prior_algo_vs_human = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="To what extent do you believe algorithms outperform humans in decision-making tasks? (1 = Not at all, 7 = Completely)",
        widget=widgets.RadioSelect
    )
    prior_llm_used_before = models.StringField(
        choices=[('yes', 'Yes'), ('no', 'No'), ('unsure', 'Not sure')],
        label="Have you used an LLM before?",
        widget=widgets.RadioSelect
    )
    prior_llm_judgment_conf = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="How confident are you in your ability to judge whether an LLM's output is reliable? (1 = Not at all confident, 7 = Extremely confident)",
        widget=widgets.RadioSelect
    )

    # Pre-interaction task
    pre_interaction_task = models.IntegerField(
        min=0, max=1000,
        label=GLOBAL_TASK_DESCRIPTION
    )

    # LLM interaction data
    io_history = models.LongStringField()

    # Post-interaction task
    post_interaction_task = models.IntegerField(
        min=0, max=1000,
        label=GLOBAL_TASK_DESCRIPTION
    )

    # --- Post-task LLM Appreciation ---
    llm_reliance = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="How much did you rely on the assistant’s response in completing the task? (1 = Not at all, 7 = Completely)",
        widget=widgets.RadioSelect
    )
    llm_confidence_post = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="How confident are you in the solution you submitted after reading the assistant’s response? (1 = Not at all confident, 7 = Extremely confident)",
        widget=widgets.RadioSelect
    )
    llm_helpfulness = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="To what extent do you believe the assistant helped improve your judgment? (1 = Not at all, 7 = Greatly)",
        widget=widgets.RadioSelect
    )
    llm_future_use_likelihood = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="How much more likely are you to use an LLM in the future based on this experience? (1 = Much less likely, 7 = Much more likely)",
        widget=widgets.RadioSelect
    )
    llm_use_again = models.StringField(
        choices=[('yes', 'Yes'), ('no', 'No'), ('unsure', 'Unsure')],
        label="Would you choose to consult the assistant again for a similar task?",
        widget=widgets.RadioSelect
    )

    # --- Decision Fairness and Transparency ---
    llm_fairness = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="To what extent did the assistant provide a fair explanation for its suggestion? (1 = Not at all fair, 7 = Extremely fair)",
        widget=widgets.RadioSelect
    )
    llm_objectivity = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="How objective did the assistant’s reasoning feel to you? (1 = Completely biased, 7 = Completely objective)",
        widget=widgets.RadioSelect
    )
    llm_understanding = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="Did you feel that you understood why the assistant made its suggestion? (1 = Not at all, 7 = Completely)",
        widget=widgets.RadioSelect
    )
    llm_decision_fairness = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="If a person were affected by your decision, how fair would it be to them? (1 = Very unfair, 7 = Very fair)",
        widget=widgets.RadioSelect
    )

    # --- Information Retention Quiz (Ultimatum Game) ---
    retention_q1 = models.StringField(
        choices=[
            ('a', 'Both players get nothing'),
            ('b', 'Only the responder gets the amount'),
            ('c', 'The proposer gets the full amount'),
            ('d', 'The responder makes a new offer'),
        ],
        label="In the Ultimatum Game, what happens if the responder rejects the offer?",
        widget=widgets.RadioSelect
    )
    retention_q2 = models.StringField(
        choices=[
            ('a', 'High stakes'),
            ('b', 'Reputation'),
            ('c', 'Unfair splits'),
            ('d', 'Random assignment'),
        ],
        label="Which factor most increases rejection rates in unfair offers?",
        widget=widgets.RadioSelect
    )
    retention_q3 = models.StringField(
        choices=[
            ('a', '10%'),
            ('b', '30%'),
            ('c', '50%'),
            ('d', '70%'),
        ],
        label="In typical experiments, what’s the most common offer made by proposers?",
        widget=widgets.RadioSelect
    )

    # --- Perceived Usefulness and Trust ---
    llm_usefulness = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="How useful was the assistant’s response for your decision-making? (1 = Not at all useful, 7 = Extremely useful)",
        widget=widgets.RadioSelect
    )
    llm_trustworthiness = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="How trustworthy was the assistant's advice? (1 = Not at all trustworthy, 7 = Extremely trustworthy)",
        widget=widgets.RadioSelect
    )
    llm_confidence_boost = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 8)],
        label="To what extent did the assistant help you feel confident in your final choice? (1 = Not at all, 7 = A great deal)",
        widget=widgets.RadioSelect
    )

    # --- Interaction Timing ---
    interrupt_latency_submit = models.IntegerField(blank=True)
    interrupt_latency_stream = models.IntegerField(blank=True)
    reflection_time = models.IntegerField(blank=True)
    interrupted_stream = models.BooleanField(blank=True)
