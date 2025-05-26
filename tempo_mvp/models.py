from otree.api import (
    BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, widgets
)
import random


class Constants(BaseConstants):
    name_in_url = 'tempo_mvp'
    players_per_group = None
    # List of task folder names
    tasks = ['test_task', 'another_task']
    num_rounds = len(tasks)
    # Experimental arms for streaming delays
    treatments = [
        'fast_start_fast_stream',
        'fast_start_slow_stream',
        'slow_start_fast_stream',
        'slow_start_slow_stream',
    ]
    # Predefined full texts to stream for each task
    task_texts = {
        'test_task': "This is the full text for Test Task streaming...",
        'another_task': "Here is the pre-made text for Another Task streaming..."
    }


class Subsession(BaseSubsession):
    def creating_session(self):
        # Only initialize once per session
        if self.round_number == 1:
            task_sequence = random.sample(Constants.tasks, len(Constants.tasks))
            self.session.vars['task_sequence'] = task_sequence
            print("Session-level task sequence:", task_sequence)
            # Assign each player to a treatment arm
            for player in self.get_players():
                player.treatment = random.choice(Constants.treatments)
                print(f"Assigned Player {player.id_in_group} treatment {player.treatment}")


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Treatment arm
    treatment = models.StringField()
    # Interaction history (JSON string) for this round's streaming task
    io_history = models.LongStringField(blank=True)
    # Latencies recorded silently
    interrupt_latency_submit = models.IntegerField(blank=True)
    interrupt_latency_stream = models.IntegerField(blank=True)
    # Example survey fields
    prior_belief_1 = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        label="Do you like to use LLM assistants?",
        widget=widgets.RadioSelect
    )

    # manually define post-task questions

    # test task
    post_survey_rating_test_task_1 = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        label="Would you like to use this assistant for future similar tasks?",
        widget=widgets.RadioSelect
    )
    # another_task
    post_survey_rating_another_task_1 = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        label="Would you hate to use this assistant for future similar tasks?",
        widget=widgets.RadioSelect
    )

    final_dv_1 = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        label="Would you use this assistant for future tasks?",
        widget=widgets.RadioSelect
    )

