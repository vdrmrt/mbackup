mbackup is a Python application to create backups with ``rdiff-backup``
and/or ``rsync``.

The backup list:
----------------
The locations to back up are stored in a file. If no file is supplied
with ``-l``, mbackup looks for ``~/.mbackup-list``. If run as root,
mbackup looks in ``/etc/mbackup-list``.

The file format used to list the directories to back up is one line per
backup location. Each line contains two or three parameters separated by
whitespace:

* the backup type, ``rdiff-backup`` or ``rsync``
* the directory to back up
* the target directory, which is optional. Relative paths are appended
  to the global target path.

Lines starting with ``#`` are ignored. Directories with whitespace must
be wrapped in double quotes.

For example:

::
  # Backup list for mbackup
  # type[rdiff-backup | rsync] directory target
  rdiff-backup /home/user/documents /backups/documents
  rsync /mnt/archive_1
  rsync "/mnt/archive 2" backups/archive

The log file:
-------------
mbackup logs its output to a file. If no log file is specified with
``--log``, mbackup uses ``/var/log/mbackup.log`` when run as root.
Otherwise it uses ``~/.mbackup.log``.
