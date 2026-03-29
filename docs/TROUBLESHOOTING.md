# Troubleshooting

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
