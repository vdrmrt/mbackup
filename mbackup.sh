#!/bin/sh
read -p "Press any key to start the backup." key;

BACKUPLIST="/home/vdrmrt/scripts/backup/to_backup.txt"
# test filename and file exists
if [ ! -f "$BACKUPLIST" ];
then
  echo "Sorry, that file (files to backup) does not exist. Please make sure the name is correct."
  exit 1
fi

BACKUPFOLDER="/media/data1/backup2"

MAXAGE="3M"
EXCLUDE_OPTIONS="--exclude-device-files"
BINARY="/usr/bin/rdiff-backup"
OTHER_OPTIONS="--print-statistics --exclude-device-files --exclude-special-files --exclude-sockets"
EXCLUDES=""

# Build a bunch of --exclude ... statements and construct
# a number of arguments to send to rdiff-backup.
for i in $EXCLUDES; do
	EXCLUDE_OPTIONS="$EXCLUDE_OPTIONS --exclude $i"
done
OPTIONS="$EXCLUDE_OPTIONS $OTHER_OPTIONS"

cat $BACKUPLIST|while read SOURCE; do	
	DESTINATION="$BACKUPFOLDER$SOURCE"
	
	# Make sure there is a valid place to put the data
	if [ -e "$DESTINATION" ]; then
		if [ ! -d "$DESTINATION" ]; then
			echo "'$DESTINATION' exists, but is not a directory, stopping."
			exit 1
		fi
	else
		mkdir -p $DESTINATION
		echo "Created $DESTINATION"
	fi
	
	# Backup
	echo -n "Backing up $SOURCE: "
	echo "Backing up $SOURCE" >> backup_log.txt
	$BINARY $OPTIONS $SOURCE $DESTINATION >> backup_log.txt

	# How did it go?
	if [ $? -eq 0 ]; then
		echo "Successfull"
		echo -n "Removing backups older than $MAXAGE: "
		echo "Removing backups older than $MAXAGE" >> backup_log.txt
		$BINARY --force --remove-older-than $MAXAGE $DESTINATION >> backup_log.txt
		if [ $? -eq 0 ]; then
			echo "Successfull"
			echo "List of increments for $SOURCE: "
			$BINARY --list-increment-sizes $DESTINATION
		else
			echo -n "Removing backups older than $MAXAGE failed, command: "
			echo "$BINARY --force --remove-older-than $MAXAGE $DESTINATION"
		fi
	else
		# It failed; don't clean up. Assume that the
		# cron system mails output to a relevant
		# recipient.
		echo "Creating backup failed, command: "
		echo "$BINARY $OPTIONS $SOURCE $DESTINATION"
	fi
	# 2 blank lines to seperate backup's
	echo
	echo
done

read -p "Backup completed." key;