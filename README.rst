mbackup is python application to create  backups with rdiff-backup
and / or rsync.

The backup list:
----------------
The locations to backup or stored in a file.
If no file is supplied to list directories to backup (option -l) mbackup
will look for .mbackup-list in the users home directory. If run as root
mbackup will look in /etc/mbackup-list.

The file format used to list the directories to backup is one line per
backup location. Each line contains two parameters separated with a
white space (space or tab): the directory to backup and the type of
backup (rdiff-backup or rsync). Lines starting with a # are ignored.
Directories with whitespace need to be wrapped in double quotes.

For example:
::
  # Backup list for mbackup
  # directory type[rdiff-backup | rsync]
  /home/user/documents rdiff-backup
  /mnt/archive_1 rsync
  "/mnt/archive 2" rsync

The log file:
-------------
mbackup logs its output to a file. If no log file is specified
(--log option) mbackup will set /var/log/mbackup.log as the log file
when run as root. When not executed as root ~/.mbackup.log is used as
the log file.
