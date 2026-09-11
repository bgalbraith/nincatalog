#!/usr/bin/env python
import os
import sys
import tempfile

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nincatalog.settings")

    # The suite must run on a bare checkout with no .env, and must never write
    # into the real media library — on the server that is /srv/nincatalog/media.
    # setdefault means a real environment always wins.
    if "test" in sys.argv:
        os.environ.setdefault(
            "DJANGO_SECRET_KEY", "insecure-test-key-not-for-deployment"
        )
        os.environ.setdefault(
            "DJANGO_MEDIA_ROOT",
            os.path.join(tempfile.gettempdir(), "nincatalog-test-media"),
        )
        # Templates render {% static %} during tests, and no manifest exists
        # until collectstatic runs.
        os.environ.setdefault("DJANGO_STATIC_MANIFEST", "false")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
