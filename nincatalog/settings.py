"""
Django settings for nincatalog project.

Deployment-specific values come from the environment; see .env.example.
Defaults reproduce the historical development configuration, so a checkout
with no .env behaves as it always has.
"""

import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# DJANGO_ENV_FILE lets the settings tests isolate themselves from a developer's
# local .env (they point it at os.devnull). Defaults to the .env beside manage.py.
environ.Env.read_env(os.environ.get("DJANGO_ENV_FILE", BASE_DIR / ".env"))

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

# Retains the *.localhost entries: merch/tests.py drives the site as
# merch.localhost, and django-hosts routes on the subdomain.
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=[
        "localhost",
        "merch.localhost",
        "admin.localhost",
        "nincatalog.com",
        "merch.nincatalog.com",
        "admin.nincatalog.com",
    ],
)

DEFAULT_APPS = [
    "model_clone",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = ["imagekit", "django_hosts"]

LOCAL_APPS = ["catalog", "merch"]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django_hosts.middleware.HostsRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_hosts.middleware.HostsResponseMiddleware",
]

ROOT_URLCONF = "nincatalog.urls"
ROOT_HOSTCONF = "nincatalog.hosts"
DEFAULT_HOST = "www"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "merch.context_processors.sidenav",
            ],
        },
    },
]

WSGI_APPLICATION = "nincatalog.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": env.str("DJANGO_DB_PATH", default=str(BASE_DIR / "db.sqlite3")),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_FORMAT = "Y-m-d"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

STATIC_URL = "/static/"
STATIC_ROOT = env.str("DJANGO_STATIC_ROOT", default=str(BASE_DIR / "staticfiles"))

# Content-hash static filenames (e.g. posters.a1b2c3d4.css) so nginx can serve
# them with a long-lived `immutable` cache header while clients still pick up
# changes immediately. Disabled for the test suite, which renders templates
# without a collectstatic manifest and asserts plain static paths.
USE_STATIC_MANIFEST = env.bool("DJANGO_STATIC_MANIFEST", default=not DEBUG)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
            if USE_STATIC_MANIFEST
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}

# Media goes to S3, served through CloudFront at DJANGO_MEDIA_DOMAIN, when a
# bucket is configured; otherwise it stays on disk under MEDIA_ROOT. Object keys
# are the same either way, so switching needs no data migration. Credentials
# come from the EC2 instance role; there are deliberately no AWS keys here.
MEDIA_S3_BUCKET = env.str("DJANGO_MEDIA_S3_BUCKET", default="")
if MEDIA_S3_BUCKET:
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": MEDIA_S3_BUCKET,
            # No default: without it every image URL would point at the private
            # bucket and 403.
            "custom_domain": env.str("DJANGO_MEDIA_DOMAIN"),
            "region_name": "us-east-1",
            "querystring_auth": False,
            # Suffix colliding names, as FileSystemStorage does. Because a name
            # is never reused, objects can be cached as immutable.
            "file_overwrite": False,
            "default_acl": None,
            "object_parameters": {
                "CacheControl": "public, max-age=31536000, immutable"
            },
        },
    }

# Generate imagekit derivatives when the source image is saved, and assume they
# exist at render time. The default (JustInTime) checks storage for every
# thumbnail on every render: cheap on disk, a network call per image on S3.
# A missing derivative renders as a broken image; `manage.py generateimages`
# repairs it.
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = "imagekit.cachefiles.strategies.Optimistic"

MEDIA_URL = "/media/"
MEDIA_ROOT = env.str("DJANGO_MEDIA_ROOT", default=str(BASE_DIR / "media"))

# nginx terminates TLS. Note that gunicorn already sets wsgi.url_scheme from
# X-Forwarded-Proto over a unix socket, so this is a backstop that makes the
# behaviour explicit rather than dependent on a gunicorn default.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

if not DEBUG:
    CSRF_TRUSTED_ORIGINS = env.list(
        "CSRF_TRUSTED_ORIGINS",
        default=[
            "https://nincatalog.com",
            "https://merch.nincatalog.com",
            "https://admin.nincatalog.com",
        ],
    )

    # Must be 0 until the DNS cutover: verification hits the real hostnames via
    # /etc/hosts, and a pin here would follow the domain back to the legacy host.
    SECURE_HSTS_SECONDS = env.int("DJANGO_HSTS_SECONDS", default=31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
    SECURE_HSTS_PRELOAD = SECURE_HSTS_SECONDS > 0

    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = False  # nginx handles the redirect

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("DJANGO_LOG_LEVEL", default="INFO"),
    },
}
