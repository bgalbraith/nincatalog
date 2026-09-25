"""Tests for the backup_db management command.

boto3 is patched: the tests capture what would be uploaded and check that it
is a gzipped, complete SQLite database.
"""

import datetime
import gzip
import os
import sqlite3
import tempfile
from pathlib import Path
from unittest import mock

from botocore.exceptions import ClientError
from django.core.management import CommandError, call_command
from django.test import SimpleTestCase

ENV = {"DJANGO_BACKUP_BUCKET": "nin-host-backups", "DJANGO_BACKUP_PREFIX": "nincatalog"}
BOTO3 = "catalog.management.commands.backup_db.boto3"


class BackupDbTests(SimpleTestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.db_path = self.tmp / "db.sqlite3"
        conn = sqlite3.connect(self.db_path)
        with conn:
            conn.execute("CREATE TABLE item (id INTEGER PRIMARY KEY, name TEXT)")
            conn.executemany(
                "INSERT INTO item (name) VALUES (?)",
                [("Pretty Hate Machine",), ("Broken",)],
            )
        conn.close()

    def run_backup(self, client):
        """Run the command and return (bucket, key, uploaded bytes)."""
        uploaded = {}

        def capture(filename, bucket, key, **kwargs):
            uploaded["args"] = (bucket, key)
            uploaded["body"] = Path(filename).read_bytes()

        client.upload_file.side_effect = capture
        with mock.patch.dict(os.environ, ENV):
            call_command("backup_db", db_path=str(self.db_path))
        return (*uploaded["args"], uploaded["body"])

    @mock.patch(BOTO3)
    def test_uploads_a_complete_gzipped_database(self, boto3):
        bucket, key, body = self.run_backup(boto3.client.return_value)

        today = datetime.datetime.now(datetime.UTC).date().isoformat()
        self.assertEqual(bucket, "nin-host-backups")
        self.assertEqual(key, f"nincatalog/db/{today}.sqlite3.gz")

        restored = self.tmp / "restored.sqlite3"
        restored.write_bytes(gzip.decompress(body))
        conn = sqlite3.connect(restored)
        self.addCleanup(conn.close)
        names = [row[0] for row in conn.execute("SELECT name FROM item ORDER BY id")]
        self.assertEqual(names, ["Pretty Hate Machine", "Broken"])

    @mock.patch(BOTO3)
    def test_missing_database_fails_instead_of_uploading_an_empty_one(self, boto3):
        """sqlite3.connect() creates missing files; a typo'd path must not
        become today's backup."""
        missing = self.tmp / "nope.sqlite3"
        with mock.patch.dict(os.environ, ENV):
            with self.assertRaises(CommandError):
                call_command("backup_db", db_path=str(missing))
        boto3.client.return_value.upload_file.assert_not_called()
        self.assertFalse(missing.exists())

    @mock.patch(BOTO3)
    def test_unset_bucket_fails(self, boto3):
        env = {**ENV, "DJANGO_BACKUP_BUCKET": ""}
        with mock.patch.dict(os.environ, env):
            with self.assertRaisesRegex(CommandError, "DJANGO_BACKUP_BUCKET"):
                call_command("backup_db", db_path=str(self.db_path))
        boto3.client.return_value.upload_file.assert_not_called()

    @mock.patch(BOTO3)
    def test_unset_prefix_fails(self, boto3):
        env = {**ENV, "DJANGO_BACKUP_PREFIX": ""}
        with mock.patch.dict(os.environ, env):
            with self.assertRaisesRegex(CommandError, "DJANGO_BACKUP_PREFIX"):
                call_command("backup_db", db_path=str(self.db_path))
        boto3.client.return_value.upload_file.assert_not_called()

    @mock.patch(BOTO3)
    def test_upload_error_fails(self, boto3):
        """A missing IAM permission must surface as a failed systemd run."""
        boto3.client.return_value.upload_file.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "denied"}}, "PutObject"
        )
        with mock.patch.dict(os.environ, ENV):
            with self.assertRaisesRegex(CommandError, "AccessDenied"):
                call_command("backup_db", db_path=str(self.db_path))

    @mock.patch(BOTO3)
    def test_corrupt_database_fails(self, boto3):
        corrupt = self.tmp / "corrupt.sqlite3"
        corrupt.write_bytes(b"not a database" * 100)
        with mock.patch.dict(os.environ, ENV):
            with self.assertRaises(CommandError):
                call_command("backup_db", db_path=str(corrupt))
        boto3.client.return_value.upload_file.assert_not_called()
