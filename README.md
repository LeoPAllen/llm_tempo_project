# llm_tempo_project
llm_tempo_project

I havn't tested the set-up on a new machine, let me know if there are problems

1. set up a virtual python environment `conda create -n llm_tempo_project` (venv is fine too)
2. install the python requirements `pip install -r requirements.txt`
3. spin up the experiment (developent) server locally (`otree devserver`)
4. navigate to the hosted experiment (probably on `localhost:8000`)

To make and test changes: make a change in the code, disconnect the server (`crtl+c`), remove the database (`rm db.sqlite3` ), cached files (`find . -name "__pycache__" -exec rm -r {} +`), and restart the server (`otree devserver`)
