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

    def test_suite_never_uses_s3(self):
        """manage.py forces disk storage for `test`, whatever the environment says."""
        from django.conf import settings

        self.assertEqual(
            settings.STORAGES["default"]["BACKEND"],
            "django.core.files.storage.FileSystemStorage",
        )


class StaticStorageTests(SimpleTestCase):
    def test_manifest_storage_used_in_production(self):
        # DJANGO_STATIC_MANIFEST is cleared because manage.py sets it to false
        # for the `test` command, and the subprocess inherits this environment.
        backend = load_setting(
            "STORAGES", DJANGO_DEBUG=None, DJANGO_STATIC_MANIFEST=None
        )["staticfiles"]["BACKEND"]
        self.assertEqual(
            backend,
            "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
        )

    def test_plain_storage_when_manifest_disabled(self):
        """The test suite renders templates without a collectstatic manifest."""
        backend = load_setting(
            "STORAGES", DJANGO_DEBUG=None, DJANGO_STATIC_MANIFEST="false"
        )["staticfiles"]["BACKEND"]
        self.assertEqual(
            backend, "django.contrib.staticfiles.storage.StaticFilesStorage"
        )

    def test_static_root_defaults_to_staticfiles_not_static(self):
        """static/ is a source tree here; collectstatic must not target it."""
        value = str(load_setting("STATIC_ROOT", DJANGO_STATIC_ROOT=None))
        self.assertTrue(value.endswith("/staticfiles"), value)


class MediaStorageTests(SimpleTestCase):
    S3 = {
        "DJANGO_MEDIA_S3_BUCKET": "nincatalog-media",
        "DJANGO_MEDIA_DOMAIN": "media.nincatalog.com",
    }

    def test_disk_storage_by_default(self):
        """Local development and CI must work without AWS."""
        default = load_setting("STORAGES", DJANGO_MEDIA_S3_BUCKET=None)["default"]
        self.assertEqual(
            default["BACKEND"], "django.core.files.storage.FileSystemStorage"
        )

    def test_s3_storage_when_bucket_is_set(self):
        default = load_setting("STORAGES", **self.S3)["default"]
        self.assertEqual(default["BACKEND"], "storages.backends.s3.S3Storage")
        self.assertEqual(
            default["OPTIONS"],
            {
                "bucket_name": "nincatalog-media",
                "custom_domain": "media.nincatalog.com",
                "region_name": "us-east-1",
                # Plain URLs, so CloudFront and browsers can cache them.
                "querystring_auth": False,
                # Names are never reused; this is what makes immutable safe.
                "file_overwrite": False,
                "default_acl": None,
                "object_parameters": {
                    "CacheControl": "public, max-age=31536000, immutable"
                },
            },
        )

    def test_bucket_without_domain_fails_at_startup(self):
        """Without the CDN domain, every image URL would be a 403 from S3."""
        with self.assertRaises(subprocess.CalledProcessError):
            load_setting(
                "STORAGES",
                DJANGO_MEDIA_S3_BUCKET="nincatalog-media",
                DJANGO_MEDIA_DOMAIN=None,
            )

    def test_imagekit_does_not_touch_storage_at_render_time(self):
        self.assertEqual(
            load_setting("IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY"),
            "imagekit.cachefiles.strategies.Optimistic",
        )


class S3StorageBehaviourTests(SimpleTestCase):
    """Exercise S3Storage with the production options, without the network."""

    def make_storage(self):
        from storages.backends.s3 import S3Storage

        return S3Storage(
            bucket_name="nincatalog-media",
            custom_domain="media.nincatalog.com",
            querystring_auth=False,
            file_overwrite=False,
        )

    def test_url_points_at_the_cdn_and_keeps_the_key(self):
        """Database rows hold keys like item_images/x.jpg; they must not change."""
        self.assertEqual(
            self.make_storage().url("item_images/front.jpg"),
            "https://media.nincatalog.com/item_images/front.jpg",
        )

    def test_colliding_upload_gets_a_new_name(self):
        """A re-uploaded filename must not overwrite a cached immutable object."""
        from unittest import mock

        from storages.backends.s3 import S3Storage

        with mock.patch.object(S3Storage, "exists", side_effect=[True, False]):
            name = self.make_storage().get_available_name(
                "product_images/shirt.jpg"
            )
        self.assertNotEqual(name, "product_images/shirt.jpg")
        self.assertTrue(name.startswith("product_images/shirt_"), name)
