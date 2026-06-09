# Career Hub — Development Plan

Source brief: [`admin/project_proposal.md`](../admin/project_proposal.md). This plan turns the brief into
small, verifiable increments. Update it when the implementation diverges.

## Current workspace (2026-10-16)

- Git repo initialised on `main`, no commits. Only the brief (`admin/project_proposal.md`) and this plan exist.
- System Python is 3.15.0. `uv` and `ollama` are installed via Homebrew.

## Guiding decisions

| Decision | Choice | Why (short) |
|---|---|---|
| Python version | **3.13** pinned via `.python-version` (uv-managed), not the system 3.15 | Streamlit and its compiled deps (pyarrow, numpy) lag new Python releases; 3.13 is well supported. Verify against PyPI wheels before locking. |
| Env + lockfile | `uv` with `pyproject.toml` + committed `uv.lock` | One tool for venv, pinning, and a reproducible lock. Apache-2.0/MIT. |
| UI | Streamlit, multipage via `st.navigation` | Required by brief. Pages: Today, Opportunities, Experience, People, Settings. |
| Database | Built-in `sqlite3`, hand-written SQL, no ORM | Brief asks for stdlib unless justified. A thin repository layer keeps SQL out of pages. |
| Migrations | Numbered `.sql` files + `PRAGMA user_version`; automatic backup before applying | Simple, transparent, no extra dependency. |
| Data location | `~/.career-hub/` by default, overridable with `CAREER_HUB_DATA_DIR` | Independent of working directory; easy to find and back up. |
| AI validation (M3) | Pydantic v2 (MIT) | Concrete need: strict validation of model JSON. Not added before M3. |
| AI runtime (M3) | Ollama HTTP API via `httpx` or stdlib `urllib`, behind one `ModelClient` interface | UI/DB never touch Ollama specifics; easy to mock in tests. |
| Tests | `pytest` | Standard, MIT. |
| Privacy | `.streamlit/config.toml`: `server.address = "localhost"`, `browser.gatherUsageStats = false` | Streamlit collects usage stats by default — must be disabled and documented. |
| Containers | **Not required** to run the app. Optional Docker/Compose packaging added in Milestone 5 as a portfolio piece | Keeps the first version simple (per the brief) while the code is written container-ready from day one, so Docker drops in later without refactoring. |

Every dependency's license is checked against its official source before install and recorded in `docs/LICENSES.md` (software and model licenses in separate sections).

## Proposed folder structure

```
career-hub/
├── pyproject.toml            # direct deps pinned
├── uv.lock                   # reproducible lock (committed)
├── .python-version
├── .gitignore                # data/, *.db, exports/, backups/, .env, models
├── .streamlit/config.toml    # localhost bind, telemetry off
├── README.md                 # setup + run commands, beginner-friendly
├── admin/project_proposal.md   # project brief
├── docs/
│   ├── PLAN.md               # this file
│   ├── LICENSES.md           # software + model licenses
│   ├── schema.md             # tables, relationships, archive vs delete rules
│   ├── decisions.md          # short log of choices and why
│   └── backup-restore.md     # (M2)
├── src/career_hub/
│   ├── app.py                # Streamlit entry: navigation + DB init
│   ├── config.py             # data dir, settings
│   ├── db/
│   │   ├── connection.py     # connect(), foreign_keys=ON, transactions
│   │   ├── migrate.py        # apply migrations/, backup first
│   │   ├── migrations/001_initial.sql ...
│   │   └── repos/            # experience.py, opportunities.py, contacts.py, actions.py ...
│   ├── logic/                # plain Python, no Streamlit
│   │   ├── today.py          # prioritisation rules (M2)
│   │   ├── backup.py         # sqlite backup API + restore (M2)
│   │   └── export.py         # versioned JSON export (M2)
│   ├── ai/                   # optional, M3+
│   │   ├── client.py         # ModelClient interface + OllamaClient
│   │   ├── prompts/          # versioned prompt templates
│   │   └── schemas.py        # Pydantic result models + ID validation
│   └── ui/
│       ├── pages/            # today.py, opportunities.py, experience.py, people.py, settings.py
│       └── components.py     # shared form helpers, empty states
├── sample_data/synthetic.json
├── scripts/seed_sample.py    # loads synthetic data into a chosen DB
├── tests/
│
│   # Added in Milestone 5 (optional packaging)
├── Dockerfile
├── compose.yaml
├── .dockerignore             # excludes data, backups, .venv, .git
└── .github/workflows/ci.yml  # tests + image build
```

## Container-ready from day one

These rules cost almost nothing in Milestones 1–4 and mean Milestone 5 is
packaging work, not a refactor:

- All environment-specific settings come from environment variables with safe
  defaults: `CAREER_HUB_DATA_DIR` (data folder), `OLLAMA_HOST` (default
  `http://localhost:11434`). No hard-coded absolute paths; use `pathlib`.
- Backup, restore, export, and seeding are runnable as plain commands
  (`python -m career_hub.backup ...`), not only from the UI, so they work
  inside a container too.
- Logs go to stdout/stderr and never contain record contents.
- The app never assumes it can write anywhere except the data directory.

## Git workflow

| Level | Git form | Example |
|---|---|---|
| Milestone | Annotated tag on `main` after acceptance checks pass | `v0.1.0` (M1), `v0.2.0` (M2), … `v0.5.0` (M5) |
| Increment (numbered step below) | Short-lived branch → pull request → merge | `m1-02-database-core`, `m2-06-today-rules` |
| Change within an increment | Small, focused commits | "Add migration runner", "Test init is idempotent" |

Rules:

1. `main` always runs and its tests pass. No direct commits to `main` after the
   initial scaffold commit.
2. One branch per increment, named `m<milestone>-<step>-<short-description>`
   (lowercase, dash-separated). Branch from an up-to-date `main`.
3. Open a pull request even when working solo. Before merging: read the full
   diff, run `uv run pytest`, and try the change in the app.
4. Size check: if a diff is too long to review comfortably in one sitting,
   split the increment. Don't go smaller than an increment — per-function
   branches are overhead without safety.
5. Merge, delete the branch, then start the next increment.
6. When a milestone's last increment is merged, run its acceptance checks, then
   tag the release (`git tag -a v0.1.0 -m "Milestone 1: working foundation"`)
   with a short note on what works and known limitations.
7. Commit messages state what changed and why. Note AI assistance honestly in PR
   descriptions (e.g. "Implemented with Claude; reviewed and tested by me").

## Milestones

Each milestone is split into increments that each leave the app runnable. After each milestone I report: what works, how it was verified, known limitations, next increment.

### Milestone 1 — Working foundation

1. **Scaffold** — verify Streamlit/pytest versions + licenses, `uv init`, pin deps, `.gitignore`, `.streamlit/config.toml`, README with exact run command (`uv run streamlit run src/career_hub/app.py`). First commit.
2. **Database core** — `config.py`, `connection.py` (foreign keys on, row factory), `migrate.py`, `001_initial.sql` with `experience` and `opportunity` tables (UUID or integer IDs, `created_at`/`updated_at`, `archived_at`). Tests: init is idempotent, restart preserves data.
3. **Navigation shell** — five pages with helpful empty states; Today/People/Settings say "coming in Milestone 2".
4. **Experience CRUD** — all brief fields incl. collaborators/AI assistance and `verification_status` (confirmed / estimate / needs verification). Create, edit, archive, permanent delete with confirmation, simple text search.
5. **Opportunity CRUD (basic)** — employer, title, description, URL, location, work arrangement, compensation (amount + currency + pay period, all nullable), deadline, status, interest, `listing_checked_at`.
6. **Rerun safety** — `st.form` submissions, a per-submit token in `session_state` so reruns can't double-insert, input preserved on validation errors. Tests in repo layer + a manual double-click check.
7. **Synthetic sample data** — `sample_data/synthetic.json` + seed script, never touching the real DB unless asked.

**Acceptance:** add + edit an experience and a job, restart, both unchanged; no duplicates on rerun; Ollama never imported.

### Milestone 2 — Usable job-search workflow

1. Migration `002`: `preference`, `contact`, `interaction`, `action`, `status_history`, link tables `opportunity_experience`, `opportunity_contact` (`ON DELETE CASCADE` on links only).
2. Preferences page section in Settings (each field allows "unknown/flexible"). Kept separate from experience.
3. People: contacts CRUD, interaction log, last-interaction derived from interactions.
4. Opportunity detail: link experiences + contacts, status changes write history, single **next action** shown prominently.
5. Actions: one table for all due dates (follow-ups, deadlines prep, etc.); complete, reschedule, pin.
6. **Today** rules in `logic/today.py` (pure functions, unit-tested): pinned → overdue → deadline within N days → user priority → actionable status. Max 3, each with a "why"; closed statuses (Rejected, Withdrawn, Archived, Offer-accepted) excluded; fewer than 3 shown if that's all there is. Backlog in a collapsed expander.
7. Search across opportunities, experience, contacts.
8. **Backup/restore + export** (before real data): `sqlite3.Connection.backup()`, restore into a temp dir test verifying relationships, versioned JSON export (`schema_version` field), `docs/backup-restore.md`.

**Acceptance:** link contact + experience to a job, set a follow-up, see it on Today, complete it, history retained; backup restores elsewhere intact.

### Milestone 3 — Local job assessment

1. Hardware check script (RAM, arch, free disk) → recommend a model size; verify the exact model's license (e.g. a Qwen3 variant under Apache-2.0) from its official model card; record in `LICENSES.md`.
2. `ModelClient` interface, `OllamaClient`, `FakeClient` for tests. Configurable model + host + timeout in Settings.
3. Assessment flow on the opportunity page: manually pick experiences + preferences, **preview exactly what will be sent**, explicit size limit with a message (no silent truncation), button-triggered only (no AI on rerun).
4. Structured output validated with Pydantic: requirements with excerpts, relevant experience IDs (checked against DB), transferable skills, gaps/questions, alignment + dealbreakers (shown separately from qualification), qualitative recommendation, suggested next action. No numeric scores.
5. Store assessment with model name, prompt version, timestamp, input snapshot/record versions; flag stale when inputs changed.
6. Failure handling: server down, model missing, timeout, malformed JSON, invalid IDs → clear message, job and inputs preserved. Prompt treats job text as untrusted data.
7. Small manual evaluation with a real (sanitised) description, documented.

### Milestone 4 — Drafting and handoff

1. `draft` table with versions: original model output kept, each edit saved as a new version.
2. Resume bullets, outreach message, interview questions/answer outlines — each claim lists supporting experience IDs; unsupported or "estimate" items flagged for review, never stated as fact.
3. README refresh: setup from scratch, architecture overview, how to swap Claude for a local coding assistant.
4. Manual walkthrough using synthetic data.

### Milestone 5 — Containerized distribution (optional, portfolio)

Goal: "clone the repo, run `docker compose up`, and it works" — on macOS,
Windows, or Linux — while native `uv run` remains the primary, documented path.
Can be pulled forward to after Milestone 2 if a portfolio demo is needed sooner.

1. **Licensing check first** — verify and record licenses for the base image
   (`python:3.13-slim`), the uv image, and `ollama/ollama`. Document that
   Docker Desktop is proprietary (free only for personal/small-business use)
   and that Podman or Docker Engine (Apache-2.0) are the fully open options.
2. **Dockerfile** — multi-stage build: install locked deps with `uv sync --frozen`
   in a builder stage, copy into a slim runtime stage. Runs as a non-root user.
   Streamlit binds `0.0.0.0` *inside* the container only; healthcheck on
   `/_stcore/health`. Telemetry stays off.
3. **compose.yaml**
   - `app` service published as `127.0.0.1:8501:8501` so it is still
     localhost-only on the host.
   - Named volume mounted at `/data` with `CAREER_HUB_DATA_DIR=/data`
     (named volumes avoid SQLite locking/performance issues on Windows bind mounts).
   - Default `OLLAMA_HOST=http://host.docker.internal:11434` to use Ollama
     running natively on the host (simplest, keeps GPU access).
   - Optional `ollama` service behind a Compose profile
     (`docker compose --profile ollama up`) with its own model volume, for a
     fully containerized setup.
4. **Data in and out** — documented commands for backup, restore, and JSON
   export from the running container to a host folder, e.g.
   `docker compose exec app python -m career_hub.backup --out /data/backups`
   then `docker compose cp`. Restore tested into a fresh volume.
5. **Sample-data demo mode** — `CAREER_HUB_SEED_SAMPLE=1` starts with synthetic
   data in a throwaway volume, so reviewers can explore without real records.
6. **CI (GitHub Actions)** — run `pytest` and build the image on every push.
   Optional for the app; useful as portfolio evidence. No runtime dependency on
   GitHub.
7. **Docs** — README "Run with Docker" section (macOS + Windows/WSL2 + Podman
   notes), an architecture diagram showing host vs. container vs. Ollama, and a
   `decisions.md` entry explaining why containers are optional.

**Acceptance:** from a fresh clone on a machine with only Docker/Podman
installed, `docker compose up` serves the app at `http://localhost:8501`; data
survives `docker compose down` / `up`; it is not reachable from another device
on the network; a backup taken from the container restores into a fresh volume
with relationships intact; an assessment works against host Ollama; and the app
still runs offline once the image and model are present.

## Data rules (apply throughout)

- Parameterised SQL only; writes inside transactions; `PRAGMA foreign_keys = ON` on every connection.
- **Archive** = hidden by default, fully recoverable. **Delete** = permanent, confirmed in UI, removes link rows, never leaves orphans.
- Unknown stays `NULL` — no invented defaults (salary, dates, outcomes).
- No record contents in logs. Document that the SQLite file is not encrypted.

## Assumptions (correct me if wrong)

1. Python 3.13 instead of the system 3.15 (compatibility, pending verification).
2. Data lives in `~/.career-hub/` by default.
3. The project itself can be MIT-licensed (needed for the "all open source" requirement).
4. Plan is committed to git; real data never is.
5. Docker is a packaging option added after Milestone 4 (or after Milestone 2
   if pulled forward), never a requirement to run the app.

## Next step

Start Milestone 1, increment 1 (scaffold + license verification) once this plan is approved.
