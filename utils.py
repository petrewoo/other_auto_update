#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import logging
from weakref import WeakKeyDictionary

logger = logging.getLogger(__name__)


class PidFile(object):

    def __init__(self):
        self._pid_file = WeakKeyDictionary()

    def __get__(self, obj, objtype):
        return self._pid_file.get(obj)

    def __set__(self, obj, value):
        """Convert file name to pid file name"""

        logger.debug('input value: {}'.format(value))
        base_name = os.path.basename(value).split('.')[0]
        self._pid_file[obj] = '/tmp/{}.pid'.format(base_name)
        logger.info('pid file: {}'.format(self._pid_file[obj]))


class Fopen(object):
    """Just like with statement of open.

    Remove file when exception occurs before end of block
    """

    def __init__(self, file_name, mode):
        self.file_name = file_name
        self.mode = mode

    def __enter__(self):
        self.f = open(self.file_name, self.mode)
        return self.f

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()
        err = exc_type, exc_value, traceback
        logger.debug('{} err info: {}'.format(self.__class__, err))
        if any(err):
            os.remove(self.file_name)
        return True


class LockFile(object):
    """Exclusvie instance for python script.

    Lock file to guarantee only one instance of script
    could be executed at same time
    """

    _pid_file = PidFile()

    def __init__(self, filename):
        self._pid_file = filename
        self.pid = None

    def __enter__(self):
        """Check and write pid file when work start"""

        if not self._is_available():
            raise SystemExit

        with Fopen(self._pid_file, 'w') as f:
            logger.debug('{}'.format(os.getpid()))
            f.write(str(os.getpid()))

    def _process_is_running(self):
        """Return pid if process is running"""

        try:
            os.kill(self.pid, 0)
        except OSError:
            return False
        else:
            return True

    def _is_available(self):
        """Check program execute state"""

        if os.path.exists(self._pid_file):
            with Fopen(self._pid_file, 'r') as f:
                try:
                    self.pid = int(f.read())
                except ValueError:
                    return False

            if self._process_is_running():
                logger.warning('Process is running, gracefully shutdown.')
                return False
            else:
                return True

        return True

    def __exit__(self, exc_type, exc_value, traceback):
        """Remove pid file when work is finished"""

        logger.debug('exc_type: {}'.format(exc_type))
        logger.debug('exc_value: {}'.format(exc_value))
        logger.debug('traceback: {}'.format(traceback))

        if os.path.exists(self._pid_file):
            os.remove(self._pid_file)

        return True


if __name__ == '__main__':
    import time
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    with LockFile(__file__):
        try:
            time.sleep(20)
        except KeyboardInterrupt:
            logger.warning('Catch KeyboardInterrupt, quit test case.')
