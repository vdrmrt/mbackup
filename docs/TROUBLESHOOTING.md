# Troubleshooting

## Missing backend executable

Before a backup job starts, mbackup now performs backend preflight checks.

That means it verifies:

* the required local backend exists
* local ``ssh`` exists for remote jobs
* the required backend exists on the remote host for remote jobs

Typical examples:

```text
Required executable rsync was not found on this system
Required executable rdiff-backup was not found on remote host alice@backup.example
```

### What to check

Check local executables:

```bash
command -v rsync
command -v rdiff-backup
command -v ssh
```

Check remote executables:

```bash
ssh YOUR_USER@YOUR_HOST 'command -v rsync'
ssh YOUR_USER@YOUR_HOST 'command -v rdiff-backup'
```

### What to do

* Install the missing backend on the local machine
* Install the missing backend on the remote machine
* For remote jobs, verify the target host is reachable and SSH access works
* If `rdiff-backup` is not practical on both sides, use `rsync` for that job

## `rdiff-backup` version mismatch

If a live backup fails with an error like:

```text
unsupported pickle protocol: 4
```

then the local and remote `rdiff-backup` installations are likely too far apart in age.

One common sign is seeing a Python 2.7 based install on one machine, for example:

```text
/usr/lib/python2.7/dist-packages/rdiff_backup/Main.py
```

### What to check

Check the local version:

```bash
which rdiff-backup
rdiff-backup --version
```

Check the remote version:

```bash
ssh YOUR_HOST 'which rdiff-backup && rdiff-backup --version'
```

### What to do

* Prefer matching `rdiff-backup` versions on both machines
* If that is not possible yet, use `rsync` for the affected backup job
* Run a dry run first whenever you change the backend for an existing job

### Useful dry run

```bash
mbackup -d -l ~/.mbackup-list /backups
```
