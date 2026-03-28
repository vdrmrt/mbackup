import tempfile
import unittest
from pathlib import Path
from unittest import mock

from mbackuplib import MbackupError, Rdiffbackup, Rsyncbackup


class BackupWrapperTests(unittest.TestCase):
    def test_rdiffbackup_builds_remote_destination_and_options(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            source.mkdir()

            backup = Rdiffbackup(source=str(source), dest="/backups", verbosity=5)
            backup.setHost("backup.example")
            backup.setUser("alice")

            self.assertEqual(
                backup.getFullDest(),
                "alice@backup.example::/backups",
            )
            self.assertEqual(
                backup._getOptions([str(source), backup.getFullDest()]),
                [
                    "rdiff-backup",
                    "-v5",
                    str(source),
                    "alice@backup.example::/backups",
                ],
            )

    def test_rsyncbackup_builds_verbose_options(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            source.mkdir()

            backup = Rsyncbackup(source=str(source), dest="/backups", verbosity=True)

            self.assertEqual(
                backup._getOptions([str(source), "/backups"]),
                ["rsync", "-a", "-z", "--delete", str(source), "/backups", "-v"],
            )

    def test_backup_uses_start_with_source_and_destination(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            source.mkdir()

            backup = Rsyncbackup(source=str(source), dest="/backups", verbosity=False)

            with mock.patch.object(backup, "start", return_value=7) as start:
                return_code = backup.backup()

            start.assert_called_once_with([str(source), "/backups"])
            self.assertEqual(return_code, 7)

    def test_relative_source_path_is_rejected(self):
        with self.assertRaises(MbackupError):
            Rsyncbackup(source="relative/path", dest="/backups", verbosity=False)

    def test_missing_absolute_source_path_is_rejected(self):
        with self.assertRaises(MbackupError):
            Rdiffbackup(
                source="/tmp/mbackup-this-path-should-not-exist",
                dest="/backups",
                verbosity=3,
            )


if __name__ == "__main__":
    unittest.main()
