""" Module that defines the Rsyncbackup class."""
from .mbackup import Mbackup
from .mbackuperror import MbackupError

class Rsyncbackup(Mbackup):
    """ Class that interfaces with the rsync program.
    This class implements the Mbackup abstract base class.
    """

    #Properties to be set by the abstract base class
    _exe = 'rsync'
    _hostSeperator = ':'

    def __init__(self,source = None,dest = None,verbosity = False):
        """ Initialize the class this overrides the parent class so we
        need to execute the parent __init__ method in here.

        Args:
            source(string): source path to backup
            dest(string): destination path of backup
            verbosity(boolean): verbose output or not
        """
        super(Rsyncbackup, self).__init__(source,dest)

        self._verbosity = verbosity

    def _getOptions(self,options):
        """ Builds the options to pass to the executable
        This method needs to be overriden by the Mbackup abstract base
        class.
        Some default options are used:

        * -a: use the archive options of rsync
        * -z: use compression
        * --delete: delete files on target that are not on the source

            Args:
                options(list)

            Returns:
                Options to pass to executable.
        """
        popenOptions = [self._exe,'-a','-z','--delete']
        popenOptions.extend(options)

        if self._verbosity:
            popenOptions.extend(['-v'])

        return popenOptions
