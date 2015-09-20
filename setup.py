#!/usr/bin/env python3

from distutils.core import setup, Command
import fileinput
import re
import os
import inspect

# files to set version number in
versionFiles = ('bin/mbackup.py','mbackuplib/__init__.py')

def getVersion():
    """ Get the version number out of the subversion version control
    system. A variable contains the HeadURL property string of svn for
    the current file. A regular expression then extracts the version out
    of the string.

    Returns:
        string: the version number trunk or in format x.x.x.
    """
    svnHeadUrl = '$HeadURL$'
    return re.search('.*/(?:.*|tags|branches)/(.*|trunk)/setup.py'
                        ,svnHeadUrl).group(1)

def setVersionNumber():
    """ replaces the __version__ = 'xxx' with version from svn """
    print('Setting version numbers.')
    with fileinput.input(files=versionFiles,inplace=1) as f:
        for line in f:
            line = re.sub(r'^(__version__ = \')(.*)(\')',
                          r'\g<1>{v}\g<3>'.format(v=getVersion()),
                          line.rstrip())
            print(line)

def getReadmMe():
    readmeFile = os.path.dirname(os.path.abspath(
                        inspect.getfile(inspect.currentframe())
                    )) + '/README.rst'
    with open(readmeFile) as readmeFile:
        readme = readmeFile.read()
    return readme

class SetVersionCommand(Command):
    description = "Custom command to set version number in sourec files"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        setVersionNumber()


setup(name='mbackup',
      version=getVersion(),
      description='mbackup tool to create backups with '
                  'rdiff-backup and rsync.',
      long_description=getReadmMe(),
      author='Maarten Vandenryt',
      author_email='vdrmrt@gmail.com',
      packages=['mbackuplib'],
      scripts=['bin/mbackup.py'],
      cmdclass={
        'setversion': SetVersionCommand
      }
     )
