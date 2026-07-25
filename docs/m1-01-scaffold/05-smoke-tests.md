# Phase 5 — `tests/test_smoke.py`: guard the scaffold's guarantees

**Goal:** `uv run pytest` proves what the scaffold promises — the package
imports, the app starts, the privacy settings are in place, and Ollama is never
loaded — so a later increment can't quietly break any of them.

## The problem this phase solves

The brief asks for "focused automated tests". Every guarantee from Phases 1–3 is
easy to lose without noticing: a bad import breaks startup, someone trims
`.streamlit/config.toml`, or a convenience import pulls in Ollama and the app no
longer works without it. These tests are the first entries in the suite every
later increment runs before merging.

## Design

### `tests/test_smoke.py`


```python
import sys
import tomllib
from pathlib import Path

from streamlit.testing.v1 import AppTest

REPO_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = REPO_ROOT / "src" / "career_hub" / "app.py"


def test_package_imports():
    import career_hub  # noqa: F401


def test_app_starts_without_errors():
    at = AppTest.from_file(str(APP_PATH)).run()
    assert not at.exception
    assert at.title[0].value == "Career Hub"


def test_app_does_not_import_ollama():
    AppTest.from_file(str(APP_PATH)).run()
    assert "ollama" not in sys.modules


def test_streamlit_privacy_config():
    config = tomllib.loads((REPO_ROOT / ".streamlit" / "config.toml").read_text())
    assert config["server"]["address"] == "localhost"
    assert config["browser"]["gatherUsageStats"] is False
```

| Test | Guards | Phase it protects |
|---|---|---|
| `test_package_imports` | `src/` layout installed correctly | [1](01-python-project-and-dependencies.md) |
| `test_streamlit_privacy_config` | Localhost bind + telemetry off | [2](02-streamlit-privacy-config.md) |
| `test_app_starts_without_errors` | Entry point runs cleanly | [3](03-app-entrypoint.md) |
| `test_app_does_not_import_ollama` | Milestone 1 "works without Ollama" | [3](03-app-entrypoint.md) |

## Why these tests look the way they do

- **`AppTest`, not launching a server.** Streamlit's built-in test harness runs
  the script in-process — fast, no ports, no browser — and reports any exception.
- **Absolute path built from `__file__`**, never a bare relative path, so the
  tests pass no matter which directory `pytest` is started from.
- **The privacy test reads the file, not Streamlit's runtime config.** It guards
  against someone deleting or editing the committed settings, which is the
  realistic failure.
- **Smoke tests only, no more.** There is no business logic yet to unit-test.
  Database tests arrive in m1-02 and use a temporary database, never real data.

## Gotchas

- **`AppTest` runs in the test process.** That's what makes the `sys.modules`
  check meaningful — anything the app imports is visible to the test.
- **Don't add `pythonpath` settings to make imports work.** If
  `import career_hub` fails in tests, the package isn't installed: run `uv sync`
  instead of patching `sys.path`.
- **`pytest` with no tests exits with code 5**, which looks like a failure. Until
  this phase lands, `uv run pytest` "failing" is expected.

## Files

- `tests/test_smoke.py` (new)

## Verification

```bash
uv run pytest -v
# → test_package_imports PASSED
# → test_app_starts_without_errors PASSED
# → test_app_does_not_import_ollama PASSED
# → test_streamlit_privacy_config PASSED
```

Prove a test can fail: temporarily set `gatherUsageStats = true` in
`.streamlit/config.toml`, rerun, and confirm `test_streamlit_privacy_config`
fails. Revert the change.

Then the fresh-clone check — the end-to-end test of the whole scaffold and the
README from [Phase 4](04-project-docs-and-agent-rules.md):

```bash
cd "$(mktemp -d)"
git clone <repo-url> career-hub && cd career-hub
uv sync && uv run pytest && uv run streamlit run src/career_hub/app.py
# → tests pass; app serves on http://localhost:8501
```
