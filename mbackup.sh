#!/bin/bash

# set colors
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
NORMAL=$(tput sgr0)

# get directory to the script directory take into account links
DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

# process arguments
while getopts ":dil:m:t:vw" opt; do
  case $opt in
    d)
      DUMMY_RUN=1
      ;;
    i)
      SHOW_INCREMENTS=1
      ;;
    l)
      if [[ $OPTARG = -* ]]; then
	echo "Option -l requires an argument." >&2
        exit 1
      else
	BACKUPLIST=$OPTARG
      fi
      ;;
    m)
      if [[ $OPTARG = -* ]]; then
	echo "Option -m requires an argument." >&2
        exit 1
      else
	MAXAGE=$OPTARG
      fi
      ;;
    t)
      if [[ $OPTARG = -* ]]; then
	echo "Option -t requires an argument." >&2
        exit 1
      else
	TARGETDIR=$OPTARG
      fi
      ;;
    v)
      VERBOSE=1
      ;;
    w)
      WAIT_FOR_START=1
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Run a command take into account verbosity and dummy runs
run_command(){
  COMMAND=$1
  SHOW_OUTPUT=$2
  if [ "$COMMAND" == "" ]; then
    echo "Internal error: command empty." >&2
    exit 1;
  fi
  if [ "$VERBOSE" == "1" ]; then
    echo -e "\nCommand: $COMMAND"
  fi
  if [ "$DUMMY_RUN" != "1" ]; then
    if [ -z "$SHOW_OUTPUT" ]; then
      $COMMAND >> $LOG
    else
      $COMMAND
    fi
  fi
}

echo "Reading backup list"
if [ -z "$BACKUPLIST" ]; then
  if [[ $EUID = "0" ]]; then
    BACKUPLIST="/etc/mbackup-list"
  else
    BACKUPLIST="$HOME/.mbackup-list"
  fi
fi
# test filename and file exists
if [ ! -f "$BACKUPLIST" ];
then
  echo "Sorry, backup list file \"$BACKUPLIST\" does not exist." >&2
  exit 1
fi
if [ "$VERBOSE" == "1" ]; then
  grep -v '^#' $BACKUPLIST
fi



# Setting log file
LOGDIR="/var/log"
LOGFILE="mbackup.log"
if [ ! -w "$LOGDIR" ]; then
  LOG="$HOME/.$LOGFILE"
else
  LOG="$LOGDIR/$LOGFILE"
fi

if [ "$VERBOSE" == "1" ]; then
  echo "Log set to: $LOG";
fi

# Setting target
if [ -z "$TARGETDIR" ]; then
  TARGETDIR="$HOME/backup"
fi
if [ ! -w "$TARGETDIR" ]; then
  echo "Target dir \"$TARGETDIR\" is not writable" >&2
  exit 1
fi
if [ "$VERBOSE" == "1" ]; then
  echo "Target dir set to: $TARGETDIR"
fi

# Setting max age
if [ -z "$MAXAGE" ]; then
  MAXAGE="3M"
fi
if [ "$VERBOSE" == "1" ]; then
  echo "Max age set to: $MAXAGE"
fi

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


# do we have to wait
if [ "$WAIT_FOR_START" == "1" ]; then
  read -p "Press any key to start the backup." key;
fi
echo "Starting backup"

grep -v '^#' $BACKUPLIST|while read SOURCE TYPE; do

  if [ ! -e "$SOURCE" ]; then
    echo "Backup source \"$SOURCE\" does not exists, skipping." >&2
    echo ""
    continue
  fi

  DESTINATION="$TARGETDIR$SOURCE"
  # Make sure there is a valid place to put the data
  if [ -e "$DESTINATION" ]; then
    if [ ! -d "$DESTINATION" ]; then
      echo "'$DESTINATION' exists, but is not a directory, stopping." >&2
      exit 1
    fi
  else
    if [ "$DUMMY_RUN" != "1" ]; then
      mkdir -p $DESTINATION
    fi
    echo "Created directory $DESTINATION"
  fi

  case $TYPE in
    rdiff-backup)
      echo -n "$TYPE backup of $SOURCE: "
      echo "Backing up $SOURCE" >> $LOG
      run_command "$BINARY_RDIFF_BACKUP $OPTIONS $SOURCE $DESTINATION"

      # How did it go?
      if [ $? -eq 0 ]; then
        echo "$GREEN[OK]$NORMAL"
        echo -n "Removing backups older than $MAXAGE: "
        echo "Removing backups older than $MAXAGE" >> $LOG
        run_command "$BINARY_RDIFF_BACKUP --force --remove-older-than $MAXAGE $DESTINATION"
        if [ $? -eq 0 ]; then
            echo "$GREEN[OK]$NORMAL"
            if [ "$SHOW_INCREMENTS" == "1" ]; then
              echo "List of increments for $SOURCE: "
              run_command "$BINARY_RDIFF_BACKUP --list-increment-sizes $DESTINATION" "SHOW_OUTPUT"
            fi
        else
            echo "Removing backups older than $MAXAGE failed." >&2
        fi
      else
	echo "$RED[FAIL]$NORMAL" >&2
      fi
      ;;
    rsync)
      echo -n "$TYPE backup of $SOURCE: "
      echo "Backing up $SOURCE" >> $LOG
      run_command "$BINARY_RSYNC -vH $SOURCE $DESTINATION"

      # How did it go?
      if [ $? -eq 0 ]; then
        echo "$GREEN[OK]$NORMAL"
      else
        echo "$RED[FAIL]$NORMAL" >&2
      fi
      ;;
    *)
      echo "Backup type not recognized, skipping." >&2
      ;;
  esac
  echo ""
done

# do we have to wait before closing
if [ "$WAIT_FOR_START" == "1" ]; then
  read -p "Backup completed." key;
fi