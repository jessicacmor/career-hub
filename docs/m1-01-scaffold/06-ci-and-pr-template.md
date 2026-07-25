# Phase 6 — `.github/workflows/ci.yml` and the PR template

**Goal:** every pull request automatically runs the same lint, format, and test
commands as the README, and every PR description walks through the merge
checklist from `development_plan.md`. CI is development tooling — the app never
depends on it.

## The problem this phase solves

The git workflow says "run `uv run pytest` before merging". A rule that relies on
remembering fails exactly when you're tired or in a hurry. CI makes the check
automatic and visible on the PR, and the template turns the merge checklist into
tick-boxes instead of something to recall.

## Design

### `.github/workflows/ci.yml` (new)


```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v7
      - run: uv sync --locked
      - run: uv run ruff check
      - run: uv run ruff format --check
      - run: uv run pytest
```

- **Triggers on `pull_request` and pushes to `main`, never push-only.** The
  check has to show *on the PR*, before merging; the `main` run confirms the
  merged result.
- **`uv sync --locked`, never a plain `uv sync`.** It fails if `uv.lock` is out
  of date with `pyproject.toml`, so a forgotten `uv lock` is caught instead of
  silently re-resolved in CI.
- **Report-only commands, never `--fix`.** CI runs what the README's "before
  pushing" line runs, so a local pass means a CI pass.
- **`permissions: contents: read`** — least privilege; the job only reads code.
- **`ubuntu-latest`, not a matrix.** One OS keeps it fast and simple; macOS and
  Windows are covered by the fresh-clone check. A matrix can be added if a
  platform-specific bug ever appears.
- **`setup-uv` reads `.python-version`**, so CI uses Python 3.14 with no extra
  config.

### `.github/pull_request_template.md` (new)

GitHub pre-fills every new PR description with it:

```markdown
## What and why

<!-- What changed, and why. Link the increment doc, e.g. docs/m1-02-database-core/. -->

## Checklist

- [ ] I read the full diff
- [ ] `uv run ruff check && uv run ruff format --check && uv run pytest` passes
- [ ] I tried the change in the running app
- [ ] Docs updated in this PR if behaviour changed (feature doc, README, ADR)
- [ ] No real personal data in code, tests, sample data, or docs

## AI assistance

<!-- e.g. "Implemented with Claude; reviewed and tested by me." -->
```

- **The checklist mirrors `development_plan.md`'s merge rules**, plus the
  no-personal-data rule from `AGENTS.md` — never a different list.
- **AI assistance gets its own section** so it's described honestly every time,
  as the brief asks.

## Why GitHub Actions is acceptable here

The brief rules out any *required* paid or proprietary service. GitHub Actions
is free for public repositories and is optional automation for development: the
app never calls it, and if it disappeared every check still runs locally with
`uv run`. Recorded in `docs/LICENSES.md` under development tooling, alongside
`actions/checkout` and `astral-sh/setup-uv` (both MIT).

## Gotchas

- **The first CI run only happens on a PR or a push to `main`.** Pushing a
  feature branch without opening a PR runs nothing — open the PR to see the check.
- **Action versions are pinned to a major tag** (`@v7` for both). Check the
  latest majors at implementation time; a major bump is a deliberate PR.
- **Secrets aren't scanned here.** GitHub's built-in secret scanning and push
  protection cover that; see the [index](README.md#key-decisions).

## Files

- `.github/workflows/ci.yml` (new)
- `.github/pull_request_template.md` (new)
- `docs/LICENSES.md` (CI actions added under development tooling)

## Verification

1. Push the branch and open a PR. The description is pre-filled with the
   template.
2. The **CI / check** job appears on the PR and passes.
3. Prove it can fail: push a commit with a deliberately mis-formatted line, see
   the `ruff format --check` step fail, then revert it and see the check go
   green.
