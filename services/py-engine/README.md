# py-engine

The Python backend of Railway Radar: a FastAPI service plus a background worker that keeps train positions in Redis. It belongs to the epic "Phase 2: Live Data Backend" (SCRUM-6). Today this folder holds the Pydantic models of the RailKit response (`app/models.py`) and sample JSON files used as mock data.

## Python version

Use **Python 3.12**. Check with:

```
python --version
```

It must print `Python 3.12.x`. Everyone uses the same version so that "it works on my machine" means the same thing for all of us. CI will use this version too.

## Set up (Windows PowerShell)

Run these from the root of the repository:

```
cd services/py-engine
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

What this does:

- `python -m venv .venv` creates a **virtual environment**: a private folder with this project's packages, so they do not mix with other projects. `.venv/` is ignored by git.
- `.venv\Scripts\Activate.ps1` switches your terminal into it. The prompt then starts with `(.venv)`.
- `pip install -r requirements.txt` installs the packages listed in the file.

Notes:

- If PowerShell says running scripts is disabled, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again. This only affects the current window.
- If your prompt shows `(base)`, that is Anaconda's default environment. Do not install this project into it. Run `conda deactivate` first, then activate `.venv`.
- On macOS or Linux, activate with `source .venv/bin/activate`.

## Check that it works

With the virtual environment active, from `services/py-engine`:

```
python -c "from app.models import RailKitResponse; print('ok')"
```

It should print `ok`.

## What is in the folder

| Path               | What it is                                                                                                                         |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `app/`             | The application code. `models.py` has the Pydantic models. `mock_railkit_*.json` are sample payloads.                              |
| `tests/`           | Empty for now. Tests and `pytest` come with the Python CI ticket (SCRUM-34).                                                       |
| `requirements.txt` | The packages we use directly, each pinned to one version.                                                                          |
| `data_seed/`       | Does not exist until you create it. Large datasets you download yourself go here (see SCRUM-13). Git ignores the JSON files in it. |

## Running the server

Not available yet. The FastAPI server and its run command are added by SCRUM-8; this section will be filled in then.

## Rules for this folder

- **Dependencies:** `requirements.txt` lists only the packages we import ourselves, with `==` versions. To add one: `pip install <name>`, look up its version with `pip list`, and add the line by hand. Do not save `pip freeze` output, because it lists dozens of packages we never use directly.
- **Secrets:** keep them in a `.env.local` file in this folder, which git ignores. Never commit a key.
- **No real RailKit calls while developing.** Use the mock files. The free tier is small.
- **Do not add `lint` or `test` scripts to a `package.json` here.** The Node CI job has no Python installed. Python checks have their own job (SCRUM-34).
