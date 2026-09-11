"""Tests for the environment-driven settings contract.

Settings are read at import time, so each case loads them in a fresh
subprocess with an explicit environment rather than mutating this one.
"""

import os
import subprocess
import sys

from django.test import SimpleTestCase


PROBE = (
    "import django; django.setup(); "
    "from django.conf import settings; "
    "print(repr(getattr(settings, {name!r}, None)))"
)


def load_setting(name, **overrides):
    """Return the value of a setting under a controlled environment.

    Pass None for a variable to *remove* it. That is how a default branch gets
    exercised: setting a variable to "" is a set empty value, not an absent one,
    and django-environ would return the empty value rather than the default.
    """
    env = dict(os.environ)
    env["DJANGO_SETTINGS_MODULE"] = "nincatalog.settings"
    # Isolate from any developer .env, which read_env would otherwise apply to
    # exactly the variables a default-branch test means to leave unset.
    env["DJANGO_ENV_FILE"] = os.devnull
    env.setdefault("DJANGO_SECRET_KEY", "probe-key")
    for key, value in overrides.items():
        if value is None:
            env.pop(key, None)
        else:
            env[key] = str(value)
    result = subprocess.run(
        [sys.executable, "-c", PROBE.format(name=name)],
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    return eval(result.stdout.strip())


class SettingsFromEnvironmentTests(SimpleTestCase):
    def test_debug_defaults_to_false(self):
        """A deployment that forgets DJANGO_DEBUG must not run in debug mode."""
        self.assertIs(load_setting("DEBUG", DJANGO_DEBUG=None), False)

    def test_debug_can_be_enabled_for_development(self):
        self.assertIs(load_setting("DEBUG", DJANGO_DEBUG="true"), True)

    def test_database_path_comes_from_environment(self):
        value = load_setting("DATABASES", DJANGO_DB_PATH="/srv/nincatalog/db.sqlite3")
        self.assertEqual(str(value["default"]["NAME"]), "/srv/nincatalog/db.sqlite3")

    def test_media_root_comes_from_environment(self):
        value = load_setting("MEDIA_ROOT", DJANGO_MEDIA_ROOT="/srv/nincatalog/media")
        self.assertEqual(str(value), "/srv/nincatalog/media")

    def test_allowed_hosts_default_supports_the_local_subdomains(self):
        """merch/tests.py drives the site as merch.localhost."""
        value = load_setting("ALLOWED_HOSTS", DJANGO_ALLOWED_HOSTS=None)
        for host in ("localhost", "merch.localhost", "admin.localhost"):
            self.assertIn(host, value)

    def test_secret_key_is_not_hardcoded(self):
        """The historical committed key must not survive anywhere in settings."""
        self.assertEqual(
            load_setting("SECRET_KEY", DJANGO_SECRET_KEY="probe-key"), "probe-key"
        )

    def test_hsts_seconds_can_be_disabled_for_pre_cutover_testing(self):
        value = load_setting(
            "SECURE_HSTS_SECONDS", DJANGO_DEBUG=None, DJANGO_HSTS_SECONDS="0"
        )
        self.assertEqual(value, 0)


class TestIsolationTests(SimpleTestCase):
    """Asserts on this process's own settings, not a probe subprocess."""

    def test_media_root_is_redirected_away_from_the_real_library(self):
        """merch tests upload images; they must not land in production media.

        manage.py points MEDIA_ROOT at a temp directory for the `test` command,
        because the suite discards its database but not the files it writes.
        """
        from django.conf import settings

        media_root = str(settings.MEDIA_ROOT)
        self.assertNotIn("/srv/", media_root)
        self.assertIn("nincatalog-test-media", media_root)
