.. mbackup documentation master file, created by
   sphinx-quickstart on Fri Sep 18 22:57:00 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mbackup's documentation!
===================================

.. include:: ../../README.rst

Command line usage:
-------------------
The installed ``mbackup`` command can be invoked from the command line
with the following options.
::
  mbackup [-h] [-d] [--debug] [-i] [--host HOST] [--user USER] [-l file]
    [--log LOG] [-m time] [-v] [--version] [-w]
    target-dir

  positional arguments:
    target-dir   directory to store the backups

  optional arguments:
    -h, --help   show this help message and exit
    -d           do a dummy run
    --debug      enable debugging output
    -i           for rdiff-backup show previous increments
    --host HOST  ssh host to backup to
    --user USER  ssh user to login to backup host
    -l file      file path of list of directories to backup
    --log LOG    set log file
    -m time      how long to keep increments for rdiff-backups
    -v           enable verbose output
    --version    show version and exit
    -w           wait on user input to start the backup

Structure:
----------

The mbackup application consists of the ``mbackuplib`` package, which
contains both the CLI implementation and the interfaces to the
``rdiff-backup`` and ``rsync`` programs. The ``bin/mbackup.py`` script
remains as a compatibility wrapper for local execution.

.. toctree::
  :maxdepth: 2

  mbackup.rst
  mbackuplib.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
