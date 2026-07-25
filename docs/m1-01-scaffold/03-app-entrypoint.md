# Phase 3 — `src/career_hub/app.py`: the smallest app that proves setup works

**Goal:** a single Streamlit page that starts cleanly from the documented
command, imports nothing but Streamlit, and tells the user what to expect next.
No database, no navigation, no Ollama.

## Why a placeholder page now

Every later increment is verified by starting the app. Getting the entry point,
run command, and config working on an empty page first means any later failure
is about the new feature, not the setup. It also gives the README a command that
works today.

## Design

- **`src/career_hub/app.py`** (new) — the Streamlit entry point:

  ```python
  """Career Hub — Streamlit entry point.

  Run from the repo root:
      uv run streamlit run src/career_hub/app.py
  """

  import streamlit as st

  st.set_page_config(page_title="Career Hub", layout="centered")

  st.title("Career Hub")
  st.write(
      "Setup works. Pages for Today, Opportunities, Experience, People, "
      "and Settings arrive in the next increments."
  )
  ```

  - **`st.set_page_config` is the first Streamlit call** — Streamlit requires it
    before any other output on the page.
  - **`layout="centered"`, not `"wide"`** — the brief asks for a calm, readable
    interface; a narrow column is easier to scan than full-width content.
  - **No `st.navigation` yet.** Pages arrive in m1-03; adding navigation to a
    one-page app would be structure without content.
  - **No imports from `career_hub.*` yet.** m1-02 adds `career_hub.config` and
    database initialisation here.

## Why this file stays thin

From m1-03 on, `app.py` only wires things together: page config, database
initialisation, and `st.navigation`. Pages live in `ui/pages/`, SQL in `db/`,
rules in `logic/`. Keeping the entry point thin from the start sets that pattern
before there's anything to tangle.

## Files

- `src/career_hub/app.py` (new)

## Verification

```bash
uv run streamlit run src/career_hub/app.py
# →   URL: http://localhost:8501
```

Open `http://localhost:8501` and see the "Career Hub" title and placeholder
text. Reload the page a few times — no errors, no duplicate content. Stop with
`Ctrl+C`. Ollama can be stopped or uninstalled; the app is unaffected.

The startup log also suggests installing Watchdog "for better performance". It
only speeds up reloading when files change during development — safe to ignore,
and listed in the README's Troubleshooting table.
