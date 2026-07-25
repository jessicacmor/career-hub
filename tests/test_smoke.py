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
