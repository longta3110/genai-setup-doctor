# Generative AI Setup Doctor

This Renew Career homework project checks whether a Windows Python environment
is prepared for Generative AI development. It performs local checks only. It
does not call an AI model, spend API credits, or print an API key.

## What the program checks

- Python 3.10 or newer is running.
- A Python virtual environment is active.
- Git has been initialized in the project.
- `python-dotenv`, `openai`, `pydantic`, and `pytest` are installed.
- Every required project file exists.
- `.env` and `.venv/` are ignored by Git.
- `OPENAI_API_KEY` and `OPENAI_MODEL` have non-placeholder local values.

## Project structure

```text
genai-setup-doctor/
├── .env                 # local secret configuration; never commit
├── .env.example         # safe configuration template
├── .gitignore
├── README.md
├── requirements.txt
├── setup_doctor.py
└── tests/
    └── test_setup_doctor.py
```

## Setup on Windows PowerShell

Open PowerShell in this project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

## Configure the local environment

The repository includes `.env.example` as a safe template. Create or edit the
local `.env` file and replace both placeholders:

```text
OPENAI_API_KEY=your_private_value
OPENAI_MODEL=your_available_model_id
```

The homework does not send an API request, but the doctor checks that the two
settings are ready for later lessons. Never place the real key in
`.env.example`, the README, screenshots, terminal output, or GitHub.

## Run the Setup Doctor

With `.venv` active, run:

```powershell
python setup_doctor.py
```

Each requirement receives `PASS` or `FAIL`. The final line displays `READY`
only when every requirement passes. Fix any failed item and run the program
again.

## Run the automated tests

```powershell
python -m pytest -q
```

The tests use temporary values and do not read or display a real API key.

## Verify secret protection

Before committing, run:

```powershell
git check-ignore -v .env
git status
```

The first command should show the `.env` rule from `.gitignore`. The second
command must not list `.env` as a file to commit.

## Publish the homework

After creating an empty GitHub repository, connect and push this local project:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/genai-setup-doctor.git
git branch -M main
git push -u origin main
```

Share the GitHub repository link in the next class.

## Expected report shape

```text
Generative AI Setup Doctor
========================================================================
[PASS] Python 3.10 or newer
[PASS] Virtual environment is active
...
========================================================================
READY: The environment passed every check.
```

## Security reminder

Adding `.env` to `.gitignore` does not remove a key that was already committed.
If a real key is exposed, revoke or rotate it immediately.
