# Scaffold — Python project, privacy config, project rules, and CI

> This is the index doc. Phases 01–06 are the build plan. Read this first.
>
> Snippets in these docs are copied from the implemented files. If the code
> changes, update the matching phase doc in the same pull request.

## Context

Career Hub is a local, single-user Streamlit + SQLite app for running a job
search (see [`development_plan.md`](../development_plan.md)). This increment
delivers the empty but correctly configured project that every later increment
builds on: a pinned Python environment, a reproducible lockfile, recorded
licenses, Streamlit locked to localhost with telemetry off, a minimal page that
proves the app starts, setup instructions, the rules AI assistants follow in this
repo, decision records, smoke tests, and CI that runs lint and tests on every
pull request.

When this increment is done, anyone can clone the repo, run two commands, and see
the app in a browser on macOS, Linux, or Windows — with no database and no Ollama.

**Out of scope** (later increments):

- Data directory, SQLite connection, migrations — **m1-02 Database core**.
- `st.navigation` and the five pages — **m1-03 Navigation shell**.
- Experience and opportunity forms — **m1-04 / m1-05 CRUD**.
- Duplicate-submit protection — **m1-06 Rerun safety**.
- Synthetic sample data — **m1-07 Sample data**.
- Dockerfile and Compose — **Milestone 5**.

## Key decisions

- **Python 3.14, not 3.13 or 3.15.** The plan originally chose 3.13 on the
  assumption that Streamlit's compiled dependencies lag new Python releases. A
  PyPI check showed Streamlit `1.66.0` (requires `>=3.11`) and its heavy
  dependencies — `pyarrow 26.0.0`, `numpy 2.5.4`, `pandas 3.0.6` — all publish
  `cp313`, `cp314`, and `cp315` wheels. 3.14 has had several bug-fix releases;
  3.15 is the newest release, and libraries added in Milestones 2–4 may not
  support it yet.
  `requires-python = ">=3.14,<3.15"` makes the choice explicit; moving to 3.15
  later is a one-line change plus a re-lock.
- **uv with a committed `uv.lock`, never `pip` + `requirements.txt`.** One tool
  creates the virtual environment, installs the right Python, resolves, and
  locks. The lock pins every transitive package with hashes, so a fresh clone
  gets byte-identical dependencies. `uv` and `uv_build` are `MIT OR Apache-2.0`.
- **`src/` layout, installed as a package — never `sys.path` hacks.** Code lives
  in `src/career_hub/` and `uv sync` installs it into the venv. `import
  career_hub.db` (m1-02 onwards) then works no matter which directory a command
  runs from, and tests import the installed package rather than a stray copy.
- **Exact `==` pins for direct dependencies, ranges never.** The brief asks for
  pinned direct dependencies. Upgrades become deliberate, reviewable diffs to
  `pyproject.toml` + `uv.lock`, not surprises.
- **Privacy is enforced by config, never by "remember to pass a flag".**
  `.streamlit/config.toml` binds to `localhost` and disables Streamlit's usage
  statistics, which are **on by default**. See
  [`02-streamlit-privacy-config.md`](02-streamlit-privacy-config.md).
- **The app starts with no database and no Ollama.** The entry point imports
  only Streamlit. A smoke test asserts `ollama` is never imported, so the
  Milestone 1 acceptance check ("works without Ollama") is guarded from day one.
- **MIT license for the project.** Short, permissive, and common for portfolio
  work; compatible with every dependency's license (Apache-2.0, MIT, BSD, PSF).
- **Ruff for linting and formatting, moderate rules — not mypy yet.** One fast
  tool, configured in `pyproject.toml`, keeps AI-written code consistent and
  catches likely bugs (`E`, `F`, `I`, `B`, `UP`, `SIM`). Type checking waits
  until there is real logic to check. See
  [`01-python-project-and-dependencies.md`](01-python-project-and-dependencies.md#ruff-configuration).
- **Project rules live in `AGENTS.md`; `CLAUDE.md` only points to it.** One
  source of truth for any AI assistant (Claude or a local one), never two copies
  that drift. Rules that can be enforced in code are — the smoke tests guard the
  privacy config and the no-Ollama rule.
- **Decisions are recorded as ADRs, not a one-line log.** Numbered files in
  `docs/adr/` with Context / Decision / Consequences. A reversed decision gets a
  *new* ADR that supersedes the old one; old ADRs are never rewritten. ADRs name
  no individuals (public repo).
- **CI checks exactly what you run locally — no auto-fix anywhere.** CI runs
  `ruff check`, `ruff format --check`, and `pytest`, the same commands the README
  lists. Running `ruff check --fix` locally is fine, but the *check* commands are
  what must pass, so "passes locally, fails in CI" can't happen.
- **GitHub Actions is development tooling, never an app dependency.** The brief
  rules out required proprietary services; CI is optional automation. If it went
  away, every check still runs locally with `uv run`.
- **Secrets: GitHub's built-in protection, no local hooks.** Secret scanning runs
  free on public repos, and push protection for your own account is on by
  default. No pre-commit or gitleaks to install and maintain.

## Reuse (do NOT rebuild)

Nothing yet — this is the first code increment. Everything here becomes the base
later increments reuse.

## Phase index

| Phase | Doc | What it covers |
|---|---|---|
| 1 | [`01-python-project-and-dependencies.md`](01-python-project-and-dependencies.md) | `.python-version`, `pyproject.toml` (incl. ruff config), `uv.lock`, `src/career_hub/__init__.py`, `docs/LICENSES.md` |
| 2 | [`02-streamlit-privacy-config.md`](02-streamlit-privacy-config.md) | `.streamlit/config.toml` — localhost bind, telemetry off, headless |
| 3 | [`03-app-entrypoint.md`](03-app-entrypoint.md) | Minimal `src/career_hub/app.py` and the run command |
| 4 | [`04-project-docs-and-agent-rules.md`](04-project-docs-and-agent-rules.md) | README (commands + troubleshooting), `LICENSE`, `.gitattributes`, commented `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `docs/adr/` |
| 5 | [`05-smoke-tests.md`](05-smoke-tests.md) | `tests/test_smoke.py` — imports, startup, privacy config, no Ollama |
| 6 | [`06-ci-and-pr-template.md`](06-ci-and-pr-template.md) | `.github/workflows/ci.yml`, `.github/pull_request_template.md` |

## Rollout order

1. **Python project and dependencies first** — nothing can be installed, run, or
   tested until `pyproject.toml` and `uv.lock` exist.
2. **Then the Streamlit config** — it must be in place *before* the app is ever
   started, so not even the first local run sends usage statistics or listens
   beyond localhost.
3. **Then the app entry point** — it needs the installed `streamlit` from step 1
   and is started under the config from step 2.
4. **Then project docs and agent rules** — the README and `AGENTS.md` document
   commands that only work once steps 1–3 exist.
5. **Then smoke tests** — they assert what steps 1–3 built, and the fresh-clone
   check follows the README from step 4 end to end.
6. **CI and PR template last** — CI runs ruff (step 1) and the tests (step 5);
   added any earlier, it would fail on missing tests. The PR template's checklist
   names the commands documented in step 4.

## Verification

From the repo root:

```bash
uv sync                                        # creates .venv with Python 3.14
uv run python --version                        # → Python 3.14.x
uv run ruff check                              # → All checks passed!
uv run ruff format --check                     # → 19 files already formatted
uv run pytest                                  # → all smoke tests pass
uv run streamlit run src/career_hub/app.py     # → serves on http://localhost:8501
```

Open `http://localhost:8501` and see the Career Hub placeholder page. Stop with
`Ctrl+C`. Then open a pull request and confirm the CI check goes green.

> **Local gotcha:** run every command from the **repo root**. Streamlit reads
> `.streamlit/config.toml` from the current working directory; starting it from
> anywhere else silently ignores the privacy settings.

## Related

- [`../development_plan.md`](../development_plan.md) — the milestone plan this
  increment belongs to.
- [`../admin/project_proposal.md`](../admin/project_proposal.md) — the original
  brief (technical direction, open source requirement, privacy rules).
