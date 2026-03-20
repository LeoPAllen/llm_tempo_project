# llm_tempo_project

oTree experiment with app flow:
`consent -> pre_tasks_measures -> tasks -> post_tasks_measures -> conclusion`

## Local setup

1. Open a terminal in this folder (`llm_tempo_project`).
2. Activate your usual Conda environment:

```bash
conda activate otree_env
```

Alternative:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies in the active environment:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Set an admin password:

```bash
export OTREE_ADMIN_PASSWORD="change-me"
```

## Run locally

```bash
otree devserver
```

Then open:
- Participant/demo links: `http://localhost:8000`
- Admin page: `http://localhost:8000/admin`

Admin login:
- Username: `admin`
- Password: value of `OTREE_ADMIN_PASSWORD`

## Reset local state

```bash
rm -f db.sqlite3
find . -name "__pycache__" -type d -prune -exec rm -rf {} +
otree devserver
```

## Deploying live

Simplest path: oTree Hub / Heroku.

Deployment files already included:
- `Procfile`
- `.python-version`
- `requirements.txt`
- `.env.example`

Required environment variables:

```bash
OTREE_ADMIN_PASSWORD=your-secure-password
OTREE_PRODUCTION=1
OTREE_AUTH_LEVEL=STUDY
```

Notes:
- `OTREE_AUTH_LEVEL=STUDY` is the safest default for a real study deployment.
- If you deploy outside Heroku and use Postgres directly, also set `DATABASE_URL`.
- Before inviting participants, do a full click-through on the deployed app and verify session creation, participant links, admin login, and export.
