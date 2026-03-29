import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock

from mbackuplib import MbackupError
from mbackuplib import cli


class CliTests(unittest.TestCase):
    def test_read_backup_list_parses_comments_and_quoted_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_list_path = Path(temp_dir) / "backup-list"
            backup_list_path.write_text(
                "# comment\n"
                'rdiff-backup "/tmp/source one" relative-target\n'
                "rsync /tmp/source-two /tmp/destination-two\n",
                encoding="utf8",
            )

            with backup_list_path.open("r", encoding="utf8") as list_file:
                backup_list = cli.readBackupList(list_file)

        self.assertEqual(
            backup_list,
            [
                ["rdiff-backup", "/tmp/source one", "relative-target"],
                ["rsync", "/tmp/source-two", "/tmp/destination-two"],
            ],
        )

    def test_read_backup_list_rejects_unknown_backup_type(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_list_path = Path(temp_dir) / "backup-list"
            backup_list_path.write_text(
                "unknown /tmp/source\n",
                encoding="utf8",
            )

            with backup_list_path.open("r", encoding="utf8") as list_file:
                with self.assertRaises(ValueError):
                    cli.readBackupList(list_file)

    def test_main_dry_run_resolves_destinations_without_running_backups(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            source_one = temp_path / "source-one"
            source_two = temp_path / "source-two"
            source_one.mkdir()
            source_two.mkdir()
            list_path = temp_path / "backup-list"
            absolute_target = temp_path / "absolute-target"
            global_target = temp_path / "global-target"
            log_path = temp_path / "mbackup.log"

            list_path.write_text(
                f'rdiff-backup "{source_one}" relative-target\n'
                f'rsync "{source_two}" "{absolute_target}"\n',
                encoding="utf8",
            )

            with list_path.open("r", encoding="utf8") as list_file:
                args = Namespace(
                    d=True,
                    debug=False,
                    i=False,
                    host="backup.example",
                    user="alice",
                    l=list_file,
                    log=str(log_path),
                    m=False,
                    v=True,
                    w=False,
                    t=str(global_target),
                )

                created_rdiff = []
                created_rsync = []

                def make_rdiffbackup(*args, **kwargs):
                    instance = mock.Mock()
                    instance.constructor_kwargs = kwargs
                    created_rdiff.append(instance)
                    return instance

                def make_rsyncbackup(*args, **kwargs):
                    instance = mock.Mock()
                    instance.constructor_kwargs = kwargs
                    created_rsync.append(instance)
                    return instance

                with mock.patch.object(cli, "parsArguments", return_value=args), \
                        mock.patch.object(cli, "createLogger", return_value=mock.Mock()), \
                        mock.patch.object(cli, "runPreflightChecks"), \
                        mock.patch.object(cli.mbackuplib, "Rdiffbackup", side_effect=make_rdiffbackup), \
                        mock.patch.object(cli.mbackuplib, "Rsyncbackup", side_effect=make_rsyncbackup):
                    cli.main()

        self.assertEqual(len(created_rdiff), 1)
        self.assertEqual(len(created_rsync), 1)
        self.assertEqual(
            created_rdiff[0].constructor_kwargs,
            {
                "source": str(source_one),
                "dest": str(global_target / "relative-target"),
                "verbosity": 5,
            },
        )
        self.assertEqual(
            created_rsync[0].constructor_kwargs,
            {
                "source": str(source_two),
                "dest": str(absolute_target),
                "verbosity": True,
            },
        )
        created_rdiff[0].backup.assert_not_called()
        created_rsync[0].backup.assert_not_called()
        created_rdiff[0].setHost.assert_called_once_with("backup.example")
        created_rdiff[0].setUser.assert_called_once_with("alice")
        created_rsync[0].setHost.assert_called_once_with("backup.example")
        created_rsync[0].setUser.assert_called_once_with("alice")

    def test_main_runs_rdiff_maintenance_after_successful_backup(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            source = temp_path / "source"
            source.mkdir()
            list_path = temp_path / "backup-list"
            global_target = temp_path / "global-target"
            log_path = temp_path / "mbackup.log"

            list_path.write_text(
                f'rdiff-backup "{source}"\n',
                encoding="utf8",
            )

            with list_path.open("r", encoding="utf8") as list_file:
                args = Namespace(
                    d=False,
                    debug=False,
                    i=True,
                    host=False,
                    user=False,
                    l=list_file,
                    log=str(log_path),
                    m="3D",
                    v=False,
                    w=False,
                    t=str(global_target),
                )

                created_rdiff = []

                def make_rdiffbackup(*args, **kwargs):
                    instance = mock.Mock()
                    instance.backup.return_value = 0
                    instance.constructor_kwargs = kwargs
                    created_rdiff.append(instance)
                    return instance

                with mock.patch.object(cli, "parsArguments", return_value=args), \
                        mock.patch.object(cli, "createLogger", return_value=mock.Mock()), \
                        mock.patch.object(cli, "runPreflightChecks"), \
                        mock.patch.object(cli.mbackuplib, "Rdiffbackup", side_effect=make_rdiffbackup):
                    cli.main()

        self.assertEqual(len(created_rdiff), 1)
        self.assertEqual(
            created_rdiff[0].constructor_kwargs,
            {
                "source": str(source),
                "dest": str(global_target / str(source).lstrip("/")),
                "verbosity": 3,
            },
        )
        created_rdiff[0].backup.assert_called_once_with()
        created_rdiff[0].remove.assert_called_once_with("3D")
        created_rdiff[0].listIncrementSizes.assert_called_once_with()

    def test_run_preflight_checks_validates_local_executable_once(self):
        verified_local = set()
        verified_remote = set()

        with mock.patch.object(cli, "checkLocalExecutable") as check_local, \
                mock.patch.object(cli, "checkRemoteExecutable") as check_remote:
            cli.runPreflightChecks(
                "rsync",
                verifiedLocal=verified_local,
                verifiedRemote=verified_remote,
            )
            cli.runPreflightChecks(
                "rsync",
                verifiedLocal=verified_local,
                verifiedRemote=verified_remote,
            )

        check_local.assert_called_once_with("rsync")
        check_remote.assert_not_called()
        self.assertEqual(verified_local, {"rsync"})
        self.assertEqual(verified_remote, set())

    def test_run_preflight_checks_validates_remote_executable_once(self):
        verified_local = set()
        verified_remote = set()

        with mock.patch.object(cli, "checkLocalExecutable") as check_local, \
                mock.patch.object(cli, "checkRemoteExecutable") as check_remote:
            cli.runPreflightChecks(
                "rdiff-backup",
                host="backup.example",
                user="alice",
                verifiedLocal=verified_local,
                verifiedRemote=verified_remote,
            )
            cli.runPreflightChecks(
                "rdiff-backup",
                host="backup.example",
                user="alice",
                verifiedLocal=verified_local,
                verifiedRemote=verified_remote,
            )

        check_local.assert_has_calls([
            mock.call("rdiff-backup"),
            mock.call("ssh"),
        ])
        check_remote.assert_called_once_with("backup.example", "alice", "rdiff-backup")
        self.assertEqual(verified_local, {"rdiff-backup", "ssh"})
        self.assertEqual(verified_remote, {("backup.example", "alice", "rdiff-backup")})

    def test_check_local_executable_raises_for_missing_command(self):
        with mock.patch.object(cli.shutil, "which", return_value=None):
            with self.assertRaises(MbackupError):
                cli.checkLocalExecutable("rsync")

    def test_check_remote_executable_raises_for_missing_remote_command(self):
        result = mock.Mock(returncode=1, stderr="not found", stdout="")

        with mock.patch.object(cli.subprocess, "run", return_value=result):
            with self.assertRaises(MbackupError):
                cli.checkRemoteExecutable("backup.example", "alice", "rsync")


if __name__ == "__main__":
    unittest.main()
