#!/usr/bin/env python3

from distutils.core import setup
import re

svnHeadUrl = '$HeadURL$'
version = re.search('.*/(?:.*|tags|branches)/(.*|trunk)/setup.py'
                    ,svnHeadUrl).group(1)

setup(name='mbackup',
      version=version,
      description='mbackup tool to create backups with '
                  'rdiff-backup and rsync.',
      author='Maarten Vandenryt',
      author_email='vdrmrt@gmail.com',
      packages=['backupapps'],
      scripts=['mbackup.py']
     )
