# Career Hub

A local-first, single-user career development hub: track job opportunities,
keep an evidence-backed bank of accomplishments, manage professional contacts,
and see a short list of the next useful actions — all on your own machine.

> **Status:** Milestone 1 in progress — the project scaffold runs, features are
> next. See the [development plan](docs/development_plan.md) for milestones.

## Why

Job searching spreads across tabs, spreadsheets, and notes. Career Hub keeps it
in one calm place and focuses on *better decisions and stronger evidence*, not
application volume:

- **One next action per opportunity**, and a **Today** view with at most three
  suggested actions, each with a plain-language reason.
- **Experience bank** that separates confirmed outcomes from estimates, so
  unverified figures never become resume claims.
- **Career preferences kept separate** from what past experience happens to
  match — a familiar role isn't automatically a good fit.
- **Optional local AI** (via Ollama) for job-fit reviews and drafts. Output is
  always an editable draft, linked to the stored evidence it relies on. No
  match scores, no hiring predictions.

## Quickstart

1. **Install uv** (manages Python and dependencies for you):
   - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
     (or `brew install uv`)
   - Windows (PowerShell):
     `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
2. **Install dependencies** — from the repo root:

   ```bash
   uv sync
   ```

   uv downloads Python 3.14 if you don't have it.
3. **Start the app:**

   ```bash
   uv run streamlit run src/career_hub/app.py
   ```

   Open <http://localhost:8501>. Stop it with `Ctrl+C` in the terminal.

Run every command from the **repo root** (the folder containing this README).

## Commands

| Command | What it does |
|---|---|
| `uv sync` | Install or update dependencies from `uv.lock` |
| `uv run streamlit run src/career_hub/app.py` | Start the app |
| `uv run pytest` | Run the tests |
| `uv run ruff check` | Lint (report only) |
| `uv run ruff format --check` | Check formatting (report only) |
| `uv run ruff check --fix && uv run ruff format` | Auto-fix lint and formatting |

Before pushing, run exactly what CI runs:

```bash
uv run ruff check && uv run ruff format --check && uv run pytest
```

## Project layout

```
career-hub/
├── src/career_hub/      # the application package
│   └── app.py           # Streamlit entry point
├── tests/               # pytest tests
├── docs/
│   ├── development_plan.md   # milestones and increments
│   ├── m1-01-scaffold/       # build plan for each increment
│   ├── adr/                  # architecture decision records
│   └── LICENSES.md           # licenses of everything used
├── .streamlit/config.toml    # localhost-only, telemetry off
├── AGENTS.md            # rules for AI assistants working in this repo
└── pyproject.toml       # dependencies and tool config
```

## Stack

| Component | Choice |
|---|---|
| Language | Python 3.14 |
| UI | Streamlit |
| Storage | SQLite (Python's built-in `sqlite3`) |
| Environment & lockfile | uv |
| Lint & format | Ruff |
| Tests | pytest |
| Local AI (optional, Milestone 3) | Ollama with an openly licensed model |
| Packaging (optional, Milestone 5) | Docker / Podman Compose |

All required components are open source; see [docs/LICENSES.md](docs/LICENSES.md).

## Privacy

- Runs on `localhost` only; no accounts, cloud services, analytics, or telemetry.
  Streamlit's usage statistics are switched off in `.streamlit/config.toml`.
- AI runs locally; there is no cloud fallback.
- Data lives in a local folder outside the repository and is never committed.
  The SQLite file is **not encrypted** — protect it like any personal document.

## Roadmap

1. Working foundation — experience and opportunity tracking
2. Job-search workflow — contacts, actions, Today, backup and export
3. Local job-fit assessment
4. Evidence-linked drafting and interview prep
5. Containerized distribution

Details and acceptance checks: [docs/development_plan.md](docs/development_plan.md).

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Privacy settings ignored; app reachable from other devices | Streamlit was started from a folder other than the repo root, so `.streamlit/config.toml` wasn't read | `cd` to the repo root and start it again |
| `ModuleNotFoundError: No module named 'career_hub'` | The package isn't installed in `.venv` | `uv sync` |
| Wrong Python version or missing packages | `python` or `streamlit` was run directly instead of through uv | Prefix the command with `uv run` |
| `uv run pytest` exits with code 5 | No tests were collected | Check you're in the repo root; tests live in `tests/` |
| Startup log suggests installing Watchdog | Optional faster file-watching for development | Safe to ignore |

## License

[MIT](LICENSE). Third-party licenses: [docs/LICENSES.md](docs/LICENSES.md).

## How this is built

Developed with AI assistance (Claude) as a pair programmer. I direct the
work, review every change, and verify each milestone with tests and manual
checks before moving on. Rules for AI assistants are in [AGENTS.md](AGENTS.md).
