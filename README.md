# llm_tempo_project

oTree experiment with app flow:
`consent -> pre_tasks_measures -> ultimatum_game -> post_tasks_measures -> conclusion`

## Local setup

1. Open a terminal in this folder (`llm_tempo_project`).
2. Activate your usual Conda environment:

```bash
conda activate otree_env
```

Alternative (if you do not want Conda for this project):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies in the active environment.

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Set an admin password for oTree.

```bash
export OTREE_ADMIN_PASSWORD="change-me"
```

## Run locally

Start the development server:

```bash
otree devserver
```

Then open:
- Participant/demo links: `http://localhost:8000`
- Admin page: `http://localhost:8000/admin` (username: `admin`, password: `OTREE_ADMIN_PASSWORD`)

## Test your changes

Typical local test loop:

1. Edit code.
2. Stop server with `Ctrl+C`.
3. (Optional clean reset) remove local db and Python cache:

```bash
rm -f db.sqlite3
find . -name "__pycache__" -type d -prune -exec rm -rf {} +
```

4. Restart with `otree devserver`.
5. Re-run through the participant flow in browser.

## Notes

- `Procfile` is for production process types (`prodserver1of2`/`prodserver2of2`), not required for local dev.
- Keep your virtual environment active whenever running `otree` commands.
