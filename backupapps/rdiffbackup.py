from .backupapp import BackupApp
from .backupapperror import BackupAppError

class Rdiffbackup(BackupApp):

    _exe = 'rdiff-backup'

    def __init__(self,source = None,dest = None,exe=None,verbosity = 3):
        super(Rdiffbackup, self).__init__(source,dest)

        self.setVerbosity(verbosity)

    def _getOptions(self,options):
        popenOptions = [self._exe,self.getVerbosityString()]
        popenOptions.extend(options)

        return popenOptions

    def backup(self):
        options = [self._source,self.getFullDest()]
        return self.start(options)

    def remove(self,time):
        options = ['--force','--remove-older-than',
                   time,self.getFullDest()]
        return self.start(options)

    def listIncrements(self):
        options = ['--list-increments',self.getFullDest()]
        return self.start(options)

    def listIncrementSizes(self):
        options = ['--list-increment-sizes',self.getFullDest()]
        return self.start(options)

    def setVerbosity(self,v):
        if v in range(0,9):
            self._verbosity = v
        else:
            raise BackupAppError('Invalid verbosity level')

    def getVerbosityString(self):
        if hasattr(self,'_verbosity'):
            return '-v' + str(self._verbosity)
