import os
import sys
import pathlib

THIS_FILE_PATH = pathlib.Path(__file__).resolve()
NBS_DIR = THIS_FILE_PATH.parent
REPO_DIR = NBS_DIR.parent
DJANGO_BASE_DIR = REPO_DIR


def init_django():
    """Boot Django from a notebook, using the same settings selection as manage.py."""
    os.chdir(DJANGO_BASE_DIR)
    sys.path.insert(0, str(DJANGO_BASE_DIR))
    from config.env import setup_settings_module
    setup_settings_module()
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"
    import django
    django.setup()
