mbackup
=======

mbackup is a Python command-line application that runs backups with
``rdiff-backup`` and/or ``rsync`` from a simple list file.

It is useful when you want one small tool to:

* read a list of backup jobs from a file
* send output to a rotating log file
* run either ``rdiff-backup`` or ``rsync`` per job
* optionally target a remote host over SSH

Requirements
------------

The Python package requires:

* Python 3.8 or newer

The backup commands themselves depend on system tools:

* ``rsync`` for ``rsync`` jobs
* ``rdiff-backup`` for ``rdiff-backup`` jobs

Installation
------------

Create a virtual environment and install the project in editable mode:

::

  python3 -m venv .venv
  . .venv/bin/activate
  python3 -m pip install -e .

After that, the installed command is:

::

  mbackup --help

For local development, the package CLI also works directly:

::

  python3 -m mbackuplib.cli --help

Quick Start
-----------

1. Create a backup list file.
2. Run a dry run first.
3. Run the real backup once the output looks right.

Example:

::

  mbackup -d -l ~/.mbackup-list /backups
  mbackup -l ~/.mbackup-list /backups

Backup List Format
------------------

The locations to back up are stored in a file. If no file is supplied
with ``-l``, mbackup looks for ``~/.mbackup-list``. If run as root,
mbackup looks in ``/etc/mbackup-list``.

The file format uses one backup job per line. Each line contains two or
three parameters separated by whitespace:

* the backup type, ``rdiff-backup`` or ``rsync``
* the directory to back up
* the target directory, which is optional. Relative paths are appended
  to the global target path

Lines starting with ``#`` are ignored. Directories with whitespace must
be wrapped in double quotes.

Example backup list:

::

  # Backup list for mbackup
  # type[rdiff-backup | rsync] directory target
  rdiff-backup /home/user/documents /backups/documents
  rsync /mnt/archive_1
  rsync "/mnt/archive 2" backups/archive

Remote Backups
--------------

You can target a remote host over SSH with ``--host`` and ``--user``:

::

  mbackup --host backup.example.com --user alice -l ~/.mbackup-list /backups

Logging
-------

mbackup logs output to a rotating log file.

If no log file is specified with ``--log``:

* root uses ``/var/log/mbackup.log``
* non-root users use ``~/.mbackup.log``

Testing
-------

Run the automated test suite with:

::

  python3 -m unittest discover -s tests -v

Documentation
-------------

The project keeps documentation lightweight and GitHub-friendly:

* ``README.rst`` is the main user-facing guide
* ``docs/DEVELOPMENT.md`` covers local development workflow
* ``docs/TROUBLESHOOTING.md`` covers operational issues such as
  ``rdiff-backup`` version mismatches

Project Layout
--------------

* ``mbackuplib/`` contains the package code
* ``mbackuplib/cli.py`` contains the main CLI implementation
* ``bin/mbackup.py`` is a compatibility wrapper for local execution
* ``docs/`` contains lightweight Markdown documentation
* ``tests/`` contains the automated tests
