from os import environ

_APP_SEQUENCE = ['consent', 'pre_tasks_measures', 'tasks', 'post_tasks_measures', 'conclusion']
_STUDY_1_PROLIFIC_COMPLETION_URL = 'TODO_STUDY_1_PROLIFIC_COMPLETION_URL'
_STUDY_1_BASE_CONFIG = dict(
    study_id='study_1',
    active_task_ids=['dictator'],
    randomize_task_order=False,
    estimated_minutes=4,
    prolific_completion_url=_STUDY_1_PROLIFIC_COMPLETION_URL,
)

SESSION_CONFIGS = [
    dict(
        name='llm_experiment',
        display_name="LLM Experiment (random assignment)",
        app_sequence=_APP_SEQUENCE,
        num_demo_participants=15,
        prolific_completion_url='https://app.prolific.com/submissions/complete?cc=CE5OTGY5',
    ),
    dict(
        name='llm_experiment_fast',
        display_name="LLM Experiment – Fast Stream",
        app_sequence=_APP_SEQUENCE,
        num_demo_participants=15,
        forced_treatment='fast_stream',
        prolific_completion_url='https://app.prolific.com/submissions/complete?cc=CE5OTGY5',
    ),
    dict(
        name='llm_experiment_slow',
        display_name="LLM Experiment – Slow Stream",
        app_sequence=_APP_SEQUENCE,
        num_demo_participants=15,
        forced_treatment='slow_stream',
        prolific_completion_url='https://app.prolific.com/submissions/complete?cc=CE5OTGY5',
    ),
    dict(
        name='llm_experiment_study_1',
        display_name='Study 1 – Dictator Task (2 x 4 random assignment)',
        app_sequence=_APP_SEQUENCE,
        num_demo_participants=8,
        **_STUDY_1_BASE_CONFIG,
    ),
    dict(
        name='llm_experiment_study_1_fast',
        display_name='Study 1 – Dictator Task, Forced Fast Stream',
        app_sequence=_APP_SEQUENCE,
        num_demo_participants=4,
        forced_treatment='fast_stream',
        **_STUDY_1_BASE_CONFIG,
    ),
    dict(
        name='llm_experiment_study_1_slow',
        display_name='Study 1 – Dictator Task, Forced Slow Stream',
        app_sequence=_APP_SEQUENCE,
        num_demo_participants=4,
        forced_treatment='slow_stream',
        **_STUDY_1_BASE_CONFIG,
    ),
    dict(
        name='llm_experiment_study_1_advice_15',
        display_name='Study 1 – Dictator Task, Forced Advice 15 USD',
        app_sequence=_APP_SEQUENCE,
        num_demo_participants=2,
        forced_advice_amount=15,
        **_STUDY_1_BASE_CONFIG,
    ),
    dict(
        name='llm_experiment_study_1_advice_25',
        display_name='Study 1 – Dictator Task, Forced Advice 25 USD',
        app_sequence=_APP_SEQUENCE,
        num_demo_participants=2,
        forced_advice_amount=25,
        **_STUDY_1_BASE_CONFIG,
    ),
    dict(
        name='llm_experiment_study_1_advice_35',
        display_name='Study 1 – Dictator Task, Forced Advice 35 USD',
        app_sequence=_APP_SEQUENCE,
        num_demo_participants=2,
        forced_advice_amount=35,
        **_STUDY_1_BASE_CONFIG,
    ),
    dict(
        name='llm_experiment_study_1_advice_45',
        display_name='Study 1 – Dictator Task, Forced Advice 45 USD',
        app_sequence=_APP_SEQUENCE,
        num_demo_participants=2,
        forced_advice_amount=45,
        **_STUDY_1_BASE_CONFIG,
    ),
]

INSTALLED_APPS = [
    'consent',
    'tasks',
    'post_tasks_measures',
    'pre_tasks_measures',
    'conclusion',
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'task_order',
    'active_task_ids',
    'llm_treatment',
    'advice_amount',
    'page_times',
    'consent_declined',
    'prolific_id',
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2609389979412'

OTREE_STYLE_CSS = '_static/global/styles.css'
