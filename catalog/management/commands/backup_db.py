"""Back up the SQLite database to S3.

Self-contained on purpose: it uses only the standard library, boto3 and
Django's DATABASES setting, and reads its configuration straight from the
environment, so another app on this host (nin.fan) can adopt it by copying this
file and the nincatalog-backup systemd units. It lives in `catalog` only
because management commands must belong to an installed app.

Environment:
    DJANGO_BACKUP_BUCKET  bucket to upload to, e.g. nin-host-backups
    DJANGO_BACKUP_PREFIX  per-app prefix, e.g. nincatalog

Uploads <prefix>/db/YYYY-MM-DD.sqlite3.gz (UTC). Credentials come from the
EC2 instance role.
"""

import datetime
import gzip
import os
import shutil
import sqlite3
import tempfile
from pathlib import Path

import boto3
from boto3.exceptions import Boto3Error
from botocore.exceptions import BotoCoreError, ClientError
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Upload a consistent, gzipped copy of the SQLite database to S3."

    def add_arguments(self, parser):
        parser.add_argument(
            "--db-path",
            default=None,
            help="Database file to back up. Defaults to DATABASES['default']['NAME'].",
        )

    def handle(self, *args, db_path=None, **options):
        bucket = os.environ.get("DJANGO_BACKUP_BUCKET", "")
        prefix = os.environ.get("DJANGO_BACKUP_PREFIX", "").strip("/")
        if not bucket:
            raise CommandError("DJANGO_BACKUP_BUCKET is not set.")
        if not prefix:
            raise CommandError("DJANGO_BACKUP_PREFIX is not set.")

        source = Path(db_path or settings.DATABASES["default"]["NAME"])
        if not source.is_file():
            # Checked explicitly: sqlite3.connect() would create an empty file.
            raise CommandError(f"Database not found: {source}")

        today = datetime.datetime.now(datetime.UTC).date().isoformat()
        key = f"{prefix}/db/{today}.sqlite3.gz"

        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp) / "snapshot.sqlite3"
            archive = Path(tmp) / "snapshot.sqlite3.gz"

            self._snapshot(source, snapshot)
            with snapshot.open("rb") as src, gzip.open(archive, "wb") as dst:
                shutil.copyfileobj(src, dst)

            try:
                boto3.client("s3").upload_file(str(archive), bucket, key)
            # upload_file re-raises a PutObject ClientError (e.g. AccessDenied)
            # as S3UploadFailedError, a Boto3Error.
            except (Boto3Error, BotoCoreError, ClientError) as exc:
                raise CommandError(f"Upload to s3://{bucket}/{key} failed: {exc}")

        self.stdout.write(f"Backed up {source} to s3://{bucket}/{key}")

    def _snapshot(self, source, target):
        """Copy with SQLite's online backup API, then verify the copy.

        The backup API yields a consistent snapshot while the site keeps
        writing, which a plain file copy does not guarantee.
        """
        try:
            src = sqlite3.connect(f"file:{source}?mode=ro", uri=True)
            dst = sqlite3.connect(target)
            try:
                src.backup(dst)
                result = dst.execute("PRAGMA integrity_check").fetchone()[0]
            finally:
                src.close()
                dst.close()
        except sqlite3.DatabaseError as exc:
            raise CommandError(f"Could not back up {source}: {exc}")
        if result != "ok":
            raise CommandError(f"Integrity check failed for {source}: {result}")
