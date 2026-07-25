# Phase 1 — `pyproject.toml`, `uv.lock`, ruff, and recorded licenses

**Goal:** a reproducible Python 3.14 environment with exactly pinned direct
dependencies, an installable `career_hub` package, lint and format rules in the
same file, and every license verified against its official source before it is
installed.

## The problem this phase solves

The machine's default `python3` is 3.15, Homebrew also has 3.13 and 3.14, and
nothing in the repo says which one the project uses. Without a pinned version
and lockfile, "works on my machine" is the best anyone can claim — and the brief
explicitly requires a reproducible lock and verified open source licenses.

## Design

- **`.python-version`** (new) — a single line, `3.14`. uv reads it and uses (or
  downloads) a matching interpreter, so nobody has to manage Python manually.
- **`pyproject.toml`** (new) — the project definition:

  ```toml
  [project]
  name = "career-hub"
  version = "0.1.0"
  description = "Local-first career development hub"
  readme = "README.md"
  license = "MIT"
  requires-python = ">=3.14,<3.15"
  dependencies = [
      "streamlit==1.66.0",
  ]

  [dependency-groups]
  dev = [
      "pytest==9.1.1",
      "ruff==0.17.1",
  ]

  [build-system]
  requires = ["uv_build>=0.13.1,<0.14"]
  build-backend = "uv_build"

  [tool.ruff]
  target-version = "py314"

  [tool.ruff.lint]
  select = ["E", "F", "I", "B", "UP", "SIM"]
  ```

  - **No `pydantic`, `httpx`, or Ollama client.** They arrive in Milestone 3,
    when there is a concrete need.
  - **`pytest` and `ruff` in a dev group, not in `dependencies`.** They are
    development tools, not something the running app needs.
  - **`uv_build` as the build backend** is what makes the `src/` package
    installable; its default layout is `src/<package_name>/`.
- **`src/career_hub/__init__.py`** (new) — empty marker file that makes
  `career_hub` a package. Later increments add `config.py`, `db/`, `ui/`, and so
  on next to it.
- **`uv.lock`** (new, generated) — produced by `uv lock`, committed, never edited
  by hand.
- **`docs/LICENSES.md`** (new) — the license register the brief requires, with
  software and model licenses in **separate sections**.

## Ruff configuration

Ruff is both the linter (finds problems) and the formatter (fixes layout). It
replaces flake8, isort, and black with one tool and one config block.

- **Moderate rules, never "everything".** The selected groups:

  | Code | What it catches |
  |---|---|
  | `E`, `F` | Style errors and real mistakes — undefined names, unused imports |
  | `I` | Import order (replaces isort) |
  | `B` | Likely bugs — mutable default arguments, `except:` that hides errors |
  | `UP` | Outdated syntax for the target Python (e.g. `Optional[X]` → `X \| None`) |
  | `SIM` | Code that can be simpler — nested `if`s, needless `else` after `return` |

  Docstring (`D`) and naming (`N`) rules are left out: on AI-written code they
  produce many warnings for little benefit. Add them later if wanted.
- **Ruff's defaults otherwise** — 88-character lines and double quotes, the same
  as black. No config means nothing to argue about.
- **`target-version = "py314"`** lets `UP` suggest the newest syntax, matching
  `requires-python`.
- **Ruff also formats Markdown.** `ruff format` (0.17) includes `.md` files and
  formats the Python code blocks inside them, which is why it reports ~19 files
  rather than 3. That's a feature here: the snippets in these docs are
  format-checked by CI, so they can't silently drift into broken examples.
- **No mypy yet.** Type checking pays off once there's real logic (Milestone 2
  onwards); a non-strict setup is added then.

## Verify licenses before installing (not after)

The brief requires checking licenses against official sources *before* install.
For each direct dependency, read the license from PyPI's JSON metadata and
confirm it against the project's own repository:

```bash
curl -s https://pypi.org/pypi/streamlit/json \
  | python3 -c "import json,sys; i=json.load(sys.stdin)['info']; print(i['version'], i.get('license_expression') or i.get('license'))"
# → 1.66.0 Apache-2.0
```

Values confirmed during planning (re-check at implementation time):

| Package | Version | License | Role |
|---|---|---|---|
| Python | 3.14 | PSF-2.0 | Runtime |
| `streamlit` | 1.66.0 | Apache-2.0 | Runtime (direct) |
| `pyarrow` | 26.0.0 | Apache-2.0 | Runtime (via Streamlit) |
| `numpy` | 2.5.4 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | Runtime (via Streamlit) |
| `pandas` | 3.0.6 | BSD-3-Clause | Runtime (via Streamlit) |
| `pytest` | 9.1.1 | MIT | Dev |
| `ruff` | 0.17.1 | MIT | Dev |
| `uv` / `uv_build` | 0.13.1 | MIT OR Apache-2.0 | Tooling / build |
| SQLite | bundled with Python | Public domain | Runtime (from m1-02) |

`docs/LICENSES.md` records **every** installed package, split into runtime
and development-only (`uv tree --no-dev` vs `uv tree --only-dev` shows which is
which). The table above is the subset that matters most. `uv.lock` remains the
source of truth for versions; regenerate the register when it changes.

> **What the full register showed:** all 42 resolved packages are under
> permissive licenses except `certifi` (MPL-2.0, file-level weak copyleft),
> which places no obligations on Career Hub when used unmodified. Streamlit
> 1.66 serves through `starlette` + `uvicorn` rather than `tornado`.

The **Models** section starts as "None — local models are added in Milestone 3"
and states up front that open weights do not imply open training data or a
reproducible training process, as the brief requires.

## Gotchas

- **The system `python3` is 3.15, not the project's 3.14.** Running `python3 -m
  pytest` or `streamlit run` directly uses the wrong interpreter and none of the
  locked packages. **Always prefix with `uv run`**, which uses `.venv`.
- **Check commands vs. fix commands.** `uv run ruff check --fix` and
  `uv run ruff format` change files; `uv run ruff check` and
  `uv run ruff format --check` only report. CI runs the report-only pair (see
  [Phase 6](06-ci-and-pr-template.md)), so run those before pushing.
- **Never hand-edit `uv.lock`.** Change `pyproject.toml`, then run `uv lock`
  (or `uv add <pkg>==<ver>`), and commit both files together.
- **`uv sync` without the dev group.** `uv sync` includes the `dev` group by
  default; `uv sync --no-dev` is the production-style install that M5's
  Dockerfile will use.

## Files

- `.python-version` (new)
- `pyproject.toml` (new)
- `uv.lock` (new, generated)
- `src/career_hub/__init__.py` (new)
- `docs/LICENSES.md` (new)

## Verification

```bash
uv lock                         # → Resolved 42 packages
uv sync                         # → creates .venv, installs career-hub (editable)
uv run python --version         # → Python 3.14.x
uv run python -c "import career_hub, streamlit; print(streamlit.__version__)"
# → 1.66.0
uv run ruff check               # → All checks passed!
uv run ruff format --check      # → 19 files already formatted
git status --short              # → uv.lock is listed; .venv/ is not (ignored)
```
