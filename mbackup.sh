#!/bin/sh
read -p "Press any key to start the backup." key;

# use escape character \ to include spaces in paths
BACKUPLIST="/home/vdrmrt/Scripts/backup/to_backup_v3.txt"
# test filename and file exists
if [ ! -f "$BACKUPLIST" ];
then
  echo "Sorry, that file (files to backup) does not exist. Please make sure the name is correct."
  exit 1
fi

BACKUPFOLDER="/media/data1/Backups"

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

cat $BACKUPLIST|while read SOURCE TYPE; do
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

  case $TYPE in
    rdiff-backup)
      echo -n "$TYPE backup of $SOURCE: "
      echo "Backing up $SOURCE" >> backup_log.txt
      $BINARY_RDIFF_BACKUP $OPTIONS $SOURCE $DESTINATION >> backup_log.txt

      # How did it go?
      if [ $? -eq 0 ]; then
        echo "Successfull"
        echo -n "Removing backups older than $MAXAGE: "
        echo "Removing backups older than $MAXAGE" >> backup_log.txt
        #$BINARY_RDIFF_BACKUP --force --remove-older-than $MAXAGE $DESTINATION >> backup_log.txt
        if [ $? -eq 0 ]; then
            echo "Successfull"
            echo "List of increments for $SOURCE: "
            $BINARY_RDIFF_BACKUP --list-increment-sizes $DESTINATION
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
      echo "Backing up $SOURCE" >> backup_log.txt
      $BINARY_RSYNC -vH $SOURCE $DESTINATION >> backup_log.txt

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
done

read -p "Backup completed." key;