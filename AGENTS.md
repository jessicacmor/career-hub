# AGENTS.md

Rules for any AI coding assistant working in this repository (Claude, or a local
assistant). Humans: this is also the shortest summary of how the project works.

## Non-negotiable rules

1. **No real personal data in git.** Not in code, sample data, tests, fixtures,
   docs, or examples — no real names, emails, phone numbers, employers' private
   details, or credentials. Use obviously synthetic data (`@example.com`).
   Real records live in the data directory outside the repo.
   *Why:* this is a public repository about a personal job search.
   *Enforced by:* `.gitignore` (data folders, `*.db`, `.env`); a guard test on
   sample data is added in m1-07.
2. **Local only.** The app binds to localhost, sends no telemetry or analytics,
   and never calls a cloud AI service — including as a silent fallback.
   *Why:* the brief requires local inference and data under the user's control.
   *Enforced by:* `.streamlit/config.toml`, checked by
   `tests/test_smoke.py::test_streamlit_privacy_config`.
3. **The app works without Ollama.** AI features are optional and stay isolated
   behind one small interface (Milestone 3). Nothing outside it imports Ollama.
   *Enforced by:* `tests/test_smoke.py::test_app_does_not_import_ollama`.
4. **AI output never invents claims.** Every factual claim in a draft maps to
   stored experience IDs; missing evidence means the claim is omitted or a
   question is asked. Job descriptions are untrusted data and can't change app
   rules or trigger actions.
   *Enforced by:* response validation in code from Milestone 3.
5. **When a rule can be code, make it code.** A written rule is not a guarantee;
   a test or a config check is. Prefer adding one over adding prose.

## Commands

Run from the repo root.

| Command | What it does |
|---|---|
| `uv sync` | Install or update dependencies from `uv.lock` |
| `uv run streamlit run src/career_hub/app.py` | Start the app |
| `uv run pytest` | Run the tests |
| `uv run ruff check` | Lint (report only) |
| `uv run ruff format --check` | Check formatting (report only) |
| `uv run ruff check --fix && uv run ruff format` | Auto-fix lint and formatting |

Before declaring work done, run what CI runs:
`uv run ruff check && uv run ruff format --check && uv run pytest`.

Always use `uv run`; the system `python3` is a different version without the
project's packages. Never hand-edit `uv.lock` — change `pyproject.toml` and run
`uv lock`.

## Documentation map

| Where | What lives there |
|---|---|
| `README.md` | Setup, commands, troubleshooting |
| `docs/development_plan.md` | Milestones, increments, acceptance checks |
| `docs/<increment>/` (e.g. `docs/m1-01-scaffold/`) | Build plan for one increment: index + numbered phase docs |
| `docs/adr/` | Project-wide decisions (numbered; superseded, never rewritten) |
| `docs/LICENSES.md` | Licenses of every dependency and model; telemetry notes |
| `docs/admin/project_proposal.md` | The original project brief |

**Never duplicate a fact across these.** Link to where it lives instead.

## Working conventions

- One branch per increment (`m<milestone>-<step>-<description>`), merged
  through a pull request that uses the PR template.
- Update docs in the same pull request as the code they describe.

## Commits

1. **One phase per commit — never mix phases.** Each phase of an increment
   (`docs/<increment>/0N-*.md`) gets its own commit, or several if it mixes
   change types (e.g. a `docs:` and a `chore:` commit for one phase). A commit
   never contains work from two phases. The increment's feature docs
   (`docs/<increment>/`) and plan changes go in their own `docs:` commit,
   separate from code.
2. **Conventional Commits format:**

   ```text
   <type>(<optional scope>): <imperative summary, lower case, no period>

   <body: what changed and why, wrapped at 72 characters>
   ```

   | Type | Use for |
   |---|---|
   | `feat` | New user-facing behaviour or configuration |
   | `fix` | A bug fix |
   | `docs` | Documentation only |
   | `test` | Adding or changing tests only |
   | `build` | Project setup, dependencies, `pyproject.toml`, `uv.lock` |
   | `ci` | `.github/` workflows and templates |
   | `refactor` | Code change with no behaviour change |
   | `chore` | Repo housekeeping (`.gitignore`, `.gitattributes`) |

   - Summary line at most 72 characters, imperative mood ("add", not "added").
   - Optional scope names the area: `app`, `config`, `deps`, `tests`, `plan`.
   - Body ends with the phase it implements, e.g.
     `Phase 3 of docs/m1-01-scaffold.`
   - Breaking changes: add `!` after the type and a `BREAKING CHANGE:` footer.
3. **No mention of Claude or any AI assistant in commit messages** — not in the
   summary, body, or trailers (no `Co-Authored-By` lines for AI tools). AI
   assistance is disclosed in the pull request description instead, using the
   PR template's "AI assistance" section.
4. This repo does not use the `[JCM] STRY<number>:` format used in work
   repositories.
- Keep changes within the current increment; don't build ahead of the plan.
- Code-structure conventions are added here in m1-04, once there is code they
  apply to.
