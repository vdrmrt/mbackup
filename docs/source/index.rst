.. mbackup documentation master file, created by
   sphinx-quickstart on Fri Sep 18 22:57:00 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mbackup's documentation!
===================================

mbackup is python application to create  backups with rdiff-backup
and / or rsync.


The mbackup application consists of two parts the mbackup script that contains the cli interface and the mbacklib package that contains that handles the rdiff-backup and rsync programs.


cli usage:
mbackup [-h] [-d] [--debug] [-i] [--host HOST] [--user USER] [-l file]
        [--log LOG] [-m time] [-v] [--version] [-w]
       target-dir

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
