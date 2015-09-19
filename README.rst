mbackup is python application to create  backups with rdiff-backup
and / or rsync.

mbackup reads a file with the locations to backup.

The file format used to list the directories to backup is one line per
backup location. Each line contains two parameters separated with a
white space (space or tab): the directory to backup and the type of
backup (rdiff-backup or rsync). Lines starting with a # are ignored.
Directories with whitespace need to be wrapped in double quotes.
For example:
# Backup list for mbackup
# directory type[rdiff-backup | rsync]
/home/user/documents rdiff-backup
/mnt/archive_1 rsync
"/mnt/archive 2" rsync

Options -i and -m are ignored for rsync backups.
