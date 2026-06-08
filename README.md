# Career Hub

A local-first, single-user career development hub: track job opportunities,
keep an evidence-backed bank of accomplishments, manage professional contacts,
and see a short list of the next useful actions — all on your own machine.

> **Status:** planning. No application code yet. See the
> [development plan](docs/PLAN.md) for milestones and progress.

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

## Planned stack

| Component | Choice |
|---|---|
| Language | Python 3.13 |
| UI | Streamlit |
| Storage | SQLite (Python's built-in `sqlite3`) |
| Environment & lockfile | uv |
| Local AI (optional, Milestone 3) | Ollama with an openly licensed model |
| Packaging (optional, Milestone 5) | Docker / Podman Compose |

All required components are open source. Licenses will be recorded in
`docs/LICENSES.md` as dependencies are added.

## Privacy

- Runs on `localhost` only; no accounts, cloud services, analytics, or telemetry.
- AI runs locally; there is no cloud fallback.
- Data lives in a local folder outside the repository and is never committed.
  The SQLite file is **not encrypted** — protect it like any personal document.

## Roadmap

1. Working foundation — experience and opportunity tracking
2. Job-search workflow — contacts, actions, Today, backup and export
3. Local job-fit assessment
4. Evidence-linked drafting and interview prep
5. Containerized distribution

Details and acceptance checks: [docs/PLAN.md](docs/PLAN.md).

## Getting started

Setup instructions will be added with Milestone 1.

## How this is built

Developed with AI assistance (Claude) as a pair programmer. I direct the
work, review every change, and verify each milestone with tests and manual
checks before moving on.
