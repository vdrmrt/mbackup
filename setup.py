#!/usr/bin/env python3

from distutils.core import setup
import re
import os
import inspect

svnHeadUrl = '$HeadURL$'
version = re.search('.*/(?:.*|tags|branches)/(.*|trunk)/setup.py'
                    ,svnHeadUrl).group(1)

def getReadmMe():
    readmeFile = os.path.dirname(os.path.abspath(
                        inspect.getfile(inspect.currentframe())
                    )) + '/README.rst'
    with open(readmeFile) as readmeFile:
        readme = readmeFile.read()
    return readme


setup(name='mbackup',
      version=version,
      description='mbackup tool to create backups with '
                  'rdiff-backup and rsync.',
      long_description=getReadmMe(),
      author='Maarten Vandenryt',
      author_email='vdrmrt@gmail.com',
      packages=['mbackuplib'],
      scripts=['mbackup.py']
     )
