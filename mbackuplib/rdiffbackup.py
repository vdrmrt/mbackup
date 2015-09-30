""" Module that defines the Rdiffbackup class."""
from .mbackup import Mbackup
from .mbackuperror import MbackupError

class Rdiffbackup(Mbackup):
    """ Class that interfaces with the rdiffbackup program.
    This class implements the Mbackup abstract base class.
    """

    #Properties to be set by the abstract base class
    _exe = 'rdiff-backup'
    _hostSeperator = '::'

    def __init__(self,source = None,dest = None,verbosity = 3):
        """ Initialize the class this overrides the parent class so we
        need to execute the parent __init__ method in here.

        Args:
            source(string): source path to backup
            dest(string): destination path of backup
            verbosity(integer): verbosity level for rdiffbackup
        """
        super(Rdiffbackup, self).__init__(source,dest)

        self.setVerbosity(verbosity)

    def _getOptions(self,options):
        """ Builds the options to pass to the executable
        This method needs to be overriden by the Mbackup abstract base
        class.
            Args:
                options(list)

            Returns:
                Options to pass to executable.
        """
        popenOptions = [self._exe,self.getVerbosityString()]
        popenOptions.extend(options)

        return popenOptions

    def remove(self,time):
        """ Starts the rdiffbackup program to remove backups older than
        the given time.

        Args:
            time(string): Rdiffbackup format of time to remove backups.

        Returns:
            Return code of rdiffbackup.
        """
        options = ['--force','--remove-older-than',
                   time,self.getFullDest()]
        return self.start(options)

    def listIncrements(self):
        """ Starts the rdiffbackup program to list all increments.

        Returns:
            Return code of rdiffbackup.
        """
        options = ['--list-increments',self.getFullDest()]
        return self.start(options)

    def listIncrementSizes(self):
        """ Lists the increment sizes.

        Returns:
            Return code of rdiffbackup.
        """
        options = ['--list-increment-sizes',self.getFullDest()]
        return self.start(options)

    def setVerbosity(self,v):
        """ Sets the verbosity level of rdiffbackup

        Raises:
            MbackupError: if verbosity level is invalid (0-9) is valid.
        """
        if v in range(0,9):
            self._verbosity = v
        else:
            raise MbackupError('Invalid verbosity level')

    def getVerbosityString(self):
        """ Builds the string of the verbosity paramater to pass to
        options of rdiffbackup.

        Returns
            String with verbosity level.
        """
        if hasattr(self,'_verbosity'):
            return '-v' + str(self._verbosity)
