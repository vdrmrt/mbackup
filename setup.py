#!/usr/bin/env python

from distutils.core import setup

svnHeadUrl = $HeadURL$
version = re.search('.*/(?:.*|tags|branches)/(.*|trunk)/setup.py'
                    ,svnHeadUrl).group(1)

setup(name='mbackup',
      version=version,
      description='mbackup tool to create backups with '
                  'rdiff-backup and rsync.',
      author='Maarten Vandenryt',
      author_email='vdrmrt@gmail.com',
      packages=['backupapps', 'distutils.command'],
      scripts=['mbackup.py']
     )
