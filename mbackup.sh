#!/bin/bash

# change working directory to the script directory take into account links
DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
cd -P $DIR

# process arguments
while getopts "diw" flag
do
  if [ "$flag" == "d" ]; then
    DUMMY_RUN=1
  fi
  if [ "$flag" == "i" ]; then
    SHOW_INCREMENTS=1
  fi
  if [ "$flag" == "w" ]; then
    WAIT_FOR_START=1
  fi
done

# do we have to wait
if [ "$WAIT_FOR_START" == "1" ]; then
  read -p "Press any key to start the backup." key;
fi

echo "Reading backup list"
# use escape character \ to include spaces in paths
BACKUPLIST="mbackup-list"
# test filename and file exists
if [ ! -f "$BACKUPLIST" ];
then
  echo "Sorry, backup list file \"$BACKUPLIST\" does not exist. Please make sure the name is correct."
  exit 1
fi

BACKUPFOLDER="/data/Backups/automated/iota"
LOG="/var/log/mbackup"

MAXAGE="3M"
EXCLUDE_OPTIONS="--exclude-device-files"
BINARY_RDIFF_BACKUP="/usr/bin/rdiff-backup"
BINARY_RSYNC="/usr/bin/rsync"
OTHER_OPTIONS="--print-statistics --exclude-device-files --exclude-special-files --exclude-sockets"
EXCLUDES=""

# Build a bunch of --exclude ... statements and construct
# a number of arguments to send to rdiff-backup.
for i in $EXCLUDES; do
        EXCLUDE_OPTIONS="$EXCLUDE_OPTIONS --exclude $i"
done
OPTIONS="$EXCLUDE_OPTIONS $OTHER_OPTIONS"

echo "Starting backup"

cat $BACKUPLIST|while read SOURCE TYPE; do
  DESTINATION="$BACKUPFOLDER$SOURCE"

  # Make sure there is a valid place to put the data
  if [ -e "$DESTINATION" ]; then
    if [ ! -d "$DESTINATION" ]; then
      echo "'$DESTINATION' exists, but is not a directory, stopping."
      exit 1
    fi
  else
    if [ "$DUMMY_RUN" != "1" ]; then
      mkdir -p $DESTINATION
    fi
    echo "Created $DESTINATION"
  fi

  case $TYPE in
    rdiff-backup)
      echo -n "$TYPE backup of $SOURCE: "
      echo "Backing up $SOURCE" >> $LOG
      if [ "$DUMMY_RUN" != "1" ]; then
	$BINARY_RDIFF_BACKUP $OPTIONS $SOURCE $DESTINATION >> $LOG
      fi

      # How did it go?
      if [ $? -eq 0 ]; then
        echo "Successfull"
        echo -n "Removing backups older than $MAXAGE: "
        echo "Removing backups older than $MAXAGE" >> $LOG
        if [ "$DUMMY_RUN" != "1" ]; then
	  $BINARY_RDIFF_BACKUP --force --remove-older-than $MAXAGE $DESTINATION >> $LOG
	fi
        if [ $? -eq 0 ]; then
            echo "Successfull"
            if [ "$SHOW_INCREMENTS" == "1" ]; then
              echo "List of increments for $SOURCE: "
              if [ "$DUMMY_RUN" != "1" ]; then
		$BINARY_RDIFF_BACKUP --list-increment-sizes $DESTINATION
	      fi
            fi
        else
            echo -n "Removing backups older than $MAXAGE failed, command: "
            echo "$BINARY_RDIFF_BACKUP --force --remove-older-than $MAXAGE $DESTINATION"
        fi
      else
        echo "Creating backup failed, command: "
        echo "$BINARY_RDIFF_BACKUP $OPTIONS $SOURCE $DESTINATION"
      fi
      ;;
    rsync)
      echo -n "$TYPE backup of $SOURCE: "
      echo "Backing up $SOURCE" >> $LOG
      if [ "$DUMMY_RUN" != "1" ]; then
	$BINARY_RSYNC -vH $SOURCE $DESTINATION >> $LOG
      fi

      # How did it go?
      if [ $? -eq 0 ]; then
        echo "Successfull"
      else
        echo "Creating backup failed, command: "
        echo " $BINARY_RSYNC -vH $SOURCE $DESTINATION"
      fi
      ;;
    *)
      echo "Backup type not recognized, skipping."
      exit
      ;;
  esac
  echo ""
done

# do we have to wait before closing
if [ "$WAIT_FOR_START" == "1" ]; then
  read -p "Backup completed." key;
fi