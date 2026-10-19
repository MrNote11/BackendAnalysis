"""Loads .env and picks the settings module: config.settings.prod when env=prod, otherwise config.settings.dev."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


def setup_settings_module():
    """Load .env from the repo root, then set DJANGO_SETTINGS_MODULE unless it is already set."""
    load_dotenv(BASE_DIR / ".env")
    if os.getenv("env", "dev") == "prod":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
