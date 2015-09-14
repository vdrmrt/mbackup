from .backupapp import BackupApp
from .backupapperror import BackupAppError

class Rsyncbackup(BackupApp):

    _exe = 'rsync'
    _hostSeperator = ':'

    def __init__(self,source = None,dest = None,verbosity = False):
        super(Rsyncbackup, self).__init__(source,dest)

        self._verbosity = verbosity

    def _getOptions(self,options):
        popenOptions = [self._exe,'-a','-z','--delete']
        popenOptions.extend(options)

        if self._verbosity:
            popenOptions.extend(['-v'])

        return popenOptions
