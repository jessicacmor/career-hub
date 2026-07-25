# Phase 4 — README, `LICENSE`, `AGENTS.md`, and ADRs

**Goal:** someone who has never seen the project can set it up from the README
alone on macOS, Linux, or Windows; any AI assistant working in the repo reads
the same non-negotiable rules; and decisions are recorded where they can't be
silently rewritten. Docs and repo metadata only — no Python code.

## The problem this phase solves

Phases 1–3 produce a working setup that only its author knows how to run, and
rules that only exist in a chat history. The brief requires "short setup
instructions and exact commands to start the app", recorded licenses, and AI
behaviour that never invents claims or leaks personal data. In a project built
mostly with an AI assistant, rules that aren't written in the repo are rules the
next session doesn't know.

## Design

### README

Restructures the root `README.md` around what a newcomer needs, in this order:
pitch → **Quickstart** → **Commands** → **Project layout** → stack → privacy →
roadmap → **Troubleshooting** → license → how this is built.

- **Quickstart** — one command per step:
  1. Install uv:
     - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
       (or `brew install uv`)
     - Windows (PowerShell):
       `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
  2. From the repo root: `uv sync` (uv fetches Python 3.14 if it's missing).
  3. `uv run streamlit run src/career_hub/app.py`, then open
     `http://localhost:8501`. Stop with `Ctrl+C`.
- **Commands** — the same table appears in `AGENTS.md`:

  | Command | What it does |
  |---|---|
  | `uv sync` | Install or update dependencies from `uv.lock` |
  | `uv run streamlit run src/career_hub/app.py` | Start the app |
  | `uv run pytest` | Run the tests |
  | `uv run ruff check` | Lint (report only) |
  | `uv run ruff format --check` | Check formatting (report only) |
  | `uv run ruff check --fix && uv run ruff format` | Auto-fix lint and formatting |

  Before pushing: `uv run ruff check && uv run ruff format --check && uv run pytest`
  — exactly what CI runs.
- **Troubleshooting** — `| Symptom | Cause | Fix |`, starting with:

  | Symptom | Cause | Fix |
  |---|---|---|
  | Privacy settings ignored; app reachable from other devices | Streamlit started from a folder other than the repo root, so `.streamlit/config.toml` wasn't read | `cd` to the repo root and start it again |
  | `ModuleNotFoundError: career_hub` | Package not installed in `.venv` | `uv sync` |
  | Wrong Python version / missing packages | Ran `python` or `streamlit` directly, not through `uv run` | Prefix commands with `uv run` |
  | `uv run pytest` exits with code 5 | No tests were collected | Check you're in the repo root; tests live in `tests/` |
  | Startup log suggests installing Watchdog | Optional faster file-watching | Safe to ignore |

  New rows are added whenever a problem costs more than a few minutes.

### `AGENTS.md` and `CLAUDE.md`

- **`AGENTS.md`** (new) — the single source of rules for any AI assistant
  (Claude now, possibly a local coding assistant later). Sections:
  1. **Non-negotiable rules**, each with *why* and *how it's enforced*:
     - **No real personal data in git** — not in code, sample data, tests,
       fixtures, docs, or examples. Synthetic data only; real records live in
       the data directory outside the repo. Enforced by `.gitignore` now, and by
       a guard test on sample data in m1-07.
     - **Local only** — bind to localhost, no telemetry or analytics, no cloud
       AI, no silent fallback to one. Enforced by the privacy smoke test.
     - **The app works without Ollama** — AI code is optional and isolated in
       `career_hub/ai/`. Enforced by the no-Ollama smoke test.
     - **AI output never invents claims** — every factual claim maps to stored
       experience IDs; job descriptions are untrusted data that can't change
       app rules. Enforced in code from Milestone 3.
     - **When a rule can be code, make it code.** A written rule is not a
       guarantee; a test is.
  2. **Commands** — the table above.
  3. **Documentation map** — where each kind of fact lives (`README.md`,
     `docs/development_plan.md`, `docs/<increment>/`, `docs/adr/`,
     `docs/LICENSES.md`), with the rule **never duplicate a fact across them**.
  4. **Working conventions** — one branch per increment, PRs with the template,
     docs and code in separate commits, update docs in the same PR as the code
     they describe.

  Code-structure conventions (thin pages, services that never call `st.*`) are
  added in m1-04, when there's code they apply to — never written ahead of the
  code they describe.
- **`CLAUDE.md`** (new) — one line, `Follow the rules in @AGENTS.md.` Never a
  second copy of the rules.

### ADRs (`docs/adr/`)

Architecture Decision Records replace the planned `docs/decisions.md`.

- **`docs/adr/000-template.md`** (new) — sections: **Status** (`Proposed |
  Accepted | Superseded by ADR-NNN`), **Context**, **Decision**,
  **Consequences**, **References**.
- **`docs/adr/001-python-3-14.md`** (new) — the first real ADR: the plan assumed
  3.13; wheel evidence showed 3.14 is safe; 3.15 is too new. Consequence:
  `requires-python = ">=3.14,<3.15"`; revisit when adding Milestone 2–4
  dependencies.
- **What gets an ADR:** a decision that changes how a future contributor
  approaches the codebase. Increment-level choices stay in that increment's
  feature README ("Key decisions"); ADRs are for project-wide ones.
- **Never edit an accepted ADR's decision.** Reversing it means a new ADR with
  `Supersedes: ADR-NNN`, and the old one's status becomes `Superseded by ADR-MMM`.
  The history of *why* is the point.
- **No individuals named** — the repo is public.

### `LICENSE`, `.gitattributes`, `.gitignore`

- **`LICENSE`** (new) — standard MIT text, `Copyright (c) 2026 Jessica C.
  Moreira`. Matches `license = "MIT"` in `pyproject.toml`.
- **`.gitattributes`** (new):

  ```gitattributes
  * text=auto eol=lf
  ```

  Stores text files with LF line endings on every OS, so Windows checkouts don't
  turn every file into a CRLF diff.
- **`.gitignore`** (changed) — a short comment on each group saying *why* it's
  ignored (e.g. "personal data — never commit"). Ignore whole folders rather than
  single files, so a new file dropped into `data/` can't be committed by accident.
  Also adds `.ruff_cache/`.

> **What implementing this surfaced:** the existing `.env.*` pattern would also
> have ignored `.env.example`, the committed template planned for m1-02 — the
> file would silently never reach the repo. Fixed with an explicit `!.env.example`
> exception; `git check-ignore -v .env.example` shows the exception matching.

## Files

- `README.md` (restructured: Quickstart, Commands, Project layout,
  Troubleshooting, License)
- `AGENTS.md` (new)
- `CLAUDE.md` (new)
- `docs/adr/000-template.md` (new)
- `docs/adr/001-python-3-14.md` (new)
- `LICENSE` (new)
- `.gitattributes` (new)
- `.gitignore` (comments added)

## Verification

```bash
git check-attr eol -- README.md        # → README.md: eol: lf
grep -c "MIT License" LICENSE          # → 1
cat CLAUDE.md                          # → one line pointing to AGENTS.md
```

Then follow the README's Quickstart exactly as written, from the repo root, and
confirm each command does what the README says. The full fresh-clone check runs
at the end of [Phase 5](05-smoke-tests.md#verification).
