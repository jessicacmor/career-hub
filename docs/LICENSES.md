# Licenses

Every component Career Hub needs must be open source (SQLite's public-domain
status is acceptable). This file records what is used and under which license.
Software and model licenses are kept in separate sections.

Licenses are checked against the official source **before** a dependency is
added: the PyPI metadata (`https://pypi.org/pypi/<package>/json`, field
`license_expression` or `license`) and the project's own repository. `uv.lock`
is the source of truth for exact versions; regenerate the tables below when it
changes.

## Software — runtime

Needed to run the app.

| Component | Version | License | Notes |
|---|---|---|---|
| Python | 3.14 | PSF-2.0 | Interpreter |
| SQLite | bundled with Python | Public domain | Database (from m1-02) |
| `streamlit` | 1.66.0 | Apache-2.0 | Direct dependency |

Installed with Streamlit (transitive):

| Package | Version | License |
|---|---|---|
| `altair` | 6.3.0 | BSD |
| `anyio` | 4.15.1 | MIT |
| `attrs` | 26.1.0 | MIT |
| `certifi` | 2026.7.22 | MPL-2.0 |
| `charset-normalizer` | 3.5.2 | MIT |
| `click` | 8.5.0 | BSD-3-Clause |
| `h11` | 0.16.0 | MIT |
| `idna` | 3.20 | BSD-3-Clause |
| `itsdangerous` | 2.2.0 | BSD |
| `jinja2` | 3.1.6 | BSD |
| `jsonschema` | 4.26.0 | MIT |
| `jsonschema-specifications` | 2025.9.1 | MIT |
| `markupsafe` | 3.0.4 | BSD-3-Clause |
| `narwhals` | 2.27.1 | MIT |
| `numpy` | 2.5.4 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 |
| `packaging` | 26.3 | Apache-2.0 OR BSD-2-Clause |
| `pandas` | 3.0.6 | BSD-3-Clause |
| `pillow` | 12.3.0 | MIT-CMU |
| `protobuf` | 7.36.2 | BSD-3-Clause |
| `pyarrow` | 26.0.0 | Apache-2.0 |
| `pydeck` | 0.9.3 | Apache-2.0 |
| `python-dateutil` | 2.9.0.post0 | BSD-3-Clause AND Apache-2.0 |
| `python-multipart` | 0.0.32 | Apache-2.0 |
| `referencing` | 0.37.0 | MIT |
| `requests` | 2.34.2 | Apache-2.0 |
| `rpds-py` | 2026.9.1 | MIT |
| `six` | 1.17.0 | MIT |
| `starlette` | 1.8.0 | BSD-3-Clause |
| `typing-extensions` | 4.16.0 | PSF-2.0 |
| `urllib3` | 2.8.0 | MIT |
| `uvicorn` | 0.54.0 | BSD-3-Clause |
| `websockets` | 17.2 | BSD-3-Clause |

`certifi` (MPL-2.0) is weak copyleft at the file level: using it unmodified
places no obligations on Career Hub's own code.

## Software — development only

Not needed to run the app.

| Component | Version | License | Role |
|---|---|---|---|
| `pytest` | 9.1.1 | MIT | Tests |
| `iniconfig` | 2.3.1 | MIT | via pytest |
| `pluggy` | 1.7.0 | MIT | via pytest |
| `pygments` | 2.21.0 | BSD-2-Clause | via pytest |
| `ruff` | 0.17.1 | MIT | Lint + format |
| `uv` | 0.13.1 | MIT OR Apache-2.0 | Environment, lockfile |
| `uv_build` | 0.13.x | MIT OR Apache-2.0 | Build backend |
| `actions/checkout` | v7 | MIT | CI (GitHub Actions) |
| `astral-sh/setup-uv` | v7 | MIT | CI (GitHub Actions) |

GitHub Actions itself is a hosted GitHub service. It is optional development
automation: the app never depends on it, and every check runs locally with
`uv run`.

## Telemetry

| Component | Telemetry | How it's disabled |
|---|---|---|
| Streamlit | Anonymous usage statistics, **on by default** | `browser.gatherUsageStats = false` in `.streamlit/config.toml`; guarded by `tests/test_smoke.py` |
| Ollama | Checked when added in Milestone 3 | — |

## Models

None yet — a local model is added in Milestone 3, with its exact name, version,
and license recorded here after checking the official model card.

Open model weights do not imply open training data or a reproducible training
process; this section records the license of the weights only.

## Project

Career Hub itself is MIT-licensed — see [`LICENSE`](../LICENSE).
