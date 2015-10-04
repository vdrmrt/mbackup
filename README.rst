mbackup is python application to create  backups with rdiff-backup
and / or rsync.

The backup list:
----------------
The locations to backup or stored in a file.
If no file is supplied to list directories to backup (option -l) mbackup
will look for .mbackup-list in the users home directory. If run as root
mbackup will look in /etc/mbackup-list.

The file format used to list the directories to backup is one line per
backup location. Each line contains two or three parameters separated
with a white space (space or tab):

* the directory to backup
* the type of backup, rdiff-backup or rsync
* the target directory, this paramater is optional. Relative paths will
  be apended to the global target path.

Lines starting with a # are ignored.
Directories with whitespace need to be wrapped in double quotes.

For example:

::
  # Backup list for mbackup
  # directory type[rdiff-backup | rsync] target
  /home/user/documents rdiff-backup /backups/documents
  /mnt/archive_1 rsync
  "/mnt/archive 2" rsync backups/archive

The log file:
-------------
mbackup logs its output to a file. If no log file is specified
(--log option) mbackup will set /var/log/mbackup.log as the log file
when run as root. When not executed as root ~/.mbackup.log is used as
the log file.
