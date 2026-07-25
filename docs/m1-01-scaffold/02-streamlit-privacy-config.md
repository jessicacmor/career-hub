# Phase 2 — `.streamlit/config.toml`: localhost only, telemetry off

**Goal:** make the brief's privacy rules the default behaviour of every run —
the app listens only on this machine and sends no usage statistics — before the
app is started for the first time. Config only; no Python code.

## The problem this phase solves

Out of the box, Streamlit:

- **collects anonymous usage statistics** (`browser.gatherUsageStats` defaults
  to `true`), and
- **listens on all network interfaces**, so anyone on the same Wi-Fi could reach
  the app at the machine's IP address.

The brief forbids both: "Bind the application to localhost by default" and "Do
not add analytics, telemetry … Document any dependency telemetry and how it is
disabled." Command-line flags would work only when someone remembers them.

## Design

- **`.streamlit/config.toml`** (new) — committed project config:

  ```toml
  # Privacy defaults required by the project brief. Do not remove.

  [server]
  # Listen on this machine only — not reachable from other devices.
  address = "localhost"
  # Don't auto-open a browser tab or show the first-run email prompt.
  headless = true

  [browser]
  # Streamlit sends anonymous usage statistics unless this is false.
  gatherUsageStats = false
  ```

  - **`address = "localhost"`, never `0.0.0.0`.** Milestone 5 binds `0.0.0.0`
    *inside the container only*, via an environment variable, and publishes the
    port as `127.0.0.1:8501:8501` — so the host stays localhost-only.
  - **`headless = true`** stops Streamlit's first-run prompt asking for an email
    address, and makes runs behave the same locally, in tests, and in containers.
- **`docs/LICENSES.md`** gets a short **Telemetry** note: Streamlit's usage
  statistics, where they are disabled, and that Ollama (M3) is checked the same
  way when it is added.

## Why a committed file (not flags or user-level config)

- **Not CLI flags** (`--server.address localhost`) — they're forgotten the first
  time someone types the short command from memory.
- **Not `~/.streamlit/config.toml`** — that lives outside the repo, so a fresh
  clone on another machine would run with telemetry on.
- **A committed project file** travels with the code and is checked by a test in
  [Phase 5](05-smoke-tests.md).

## Gotchas

> **Local gotcha:** Streamlit loads `.streamlit/config.toml` from the **current
> working directory**, not from the script's folder. Running
> `uv run streamlit run src/career_hub/app.py` from the repo root picks it up;
> running from `src/` silently falls back to the defaults. The README tells users
> to run from the repo root.

- **Environment variables override the file.** Every option has an equivalent
  such as `STREAMLIT_SERVER_ADDRESS` or `STREAMLIT_BROWSER_GATHER_USAGE_STATS`.
  This is the mechanism Milestone 5 uses inside the container; it also means a
  stray environment variable could re-enable something, which the URL in the
  startup log makes visible.
- **`.streamlit/secrets.toml` stays ignored.** It's already in `.gitignore`; only
  `config.toml` is committed.

## Files

- `.streamlit/config.toml` (new)
- `docs/LICENSES.md` (Telemetry note added)

## Verification

```bash
uv run streamlit config show   # prints the effective config
# check: server.address = "localhost"
#        server.headless = true
#        browser.gatherUsageStats = false
```

After Phase 3, start the app. The log shows a single URL line and no
`Network URL` / `External URL`:

```text
Uvicorn server started on localhost:8501
  You can now view your Streamlit app in your browser.
  URL: http://localhost:8501
```

`lsof -nP -iTCP:8501 -sTCP:LISTEN` confirms it listens on `127.0.0.1:8501`
only.
