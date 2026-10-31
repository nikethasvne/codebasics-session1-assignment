# Workout Planner

A Streamlit app that collects your fitness details and uses Groq to generate a personalized workout plan.

This is the CodeBasics session 1 assignment.

## What it does

You enter profile and training details, then click **Generate Workout Plan**. The app sends that information to a Groq chat model and displays the plan in the browser.

Inputs include:

- Name, age, weight, and height
- Gender and activity level
- Goal and time frame
- Equipment and location
- Days available per week
- Injuries or limitations

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- A [Groq API key](https://console.groq.com/)

## Setup

```bash
git clone https://github.com/nikethasvne/codebasics-session1-assignment.git
cd codebasics-session1-assignment
uv sync
```

Create a `.env` file in the project root (this file is gitignored):

```bash
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

`GROQ_MODEL` is optional. If you omit it, the app uses `openai/gpt-oss-20b`.

## Run

```bash
uv run streamlit run src/workout_planner.py
```

The app opens at [http://localhost:8501](http://localhost:8501).

## Project layout

```text
.
├── src/workout_planner.py   # Streamlit UI and Groq call
├── pyproject.toml           # Project metadata and dependencies
├── uv.lock                  # Locked dependency versions
├── .python-version          # Python 3.13
└── .env                     # Local secrets (not committed)
```

## Dependencies

Managed with uv in `pyproject.toml`:

- `streamlit` — web UI
- `groq` — Groq API client
- `python-dotenv` — loads `.env` into the environment
