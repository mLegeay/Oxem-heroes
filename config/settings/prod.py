"""Fichier de configuration pour la production."""

from .base import *
from django.core.exceptions import ImproperlyConfigured

try:
    from . import settings
except ImportError:
    raise ImproperlyConfigured("Create a settings.py file in settings")


def get_dev_setting(setting):
    """Get the setting or return exception."""
    try:
        return getattr(settings, setting)
    except AttributeError:
        error_msg = "The %s setting is missing from prod settings" % setting
        raise ImproperlyConfigured(error_msg)

DEBUG = False
ALLOWED_HOSTS = []

SECRET_KEY = get_dev_setting('SECRET_KEY')
DATABASES = get_dev_setting('DATABASES')
