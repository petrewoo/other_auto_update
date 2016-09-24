#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class PidFile(object):

    def __init__(self):
        self._pid_file = ''

    def __get__(self, obj, objtype):
        return self._pid_file

    def __set__(self, obj, value):
        """Convert file name to pid file"""

        logger.debug('input value: {}'.format(value))
        base_name = os.path.basename(value).split('.')[0]
        # TODO check base_name process need add
        self._pid_file = '/tmp/{}.pid'.format(base_name)
        logger.debug('pid file: {}'.format(self._pid_file))


class ExclusvieWapper(object):

    _pid_file = PidFile()

    def __init__(self, filename):
        self._pid_file = filename

    @contextmanager
    def exclusvie_check(self):
        """Exclusvie instance for python script

        This is a utiltiy which guarantee only one instance of script
        could be executed at same time"""

        self._setup()
        try:
            yield
        finally:
            self._cleanup()

    def _process_is_running(self):
        """Return pid if process is running"""

        try:
            os.kill(self.pid, 0)
        except OSError:
            return None
        else:
            return self.pid

    def _check_is_alive(self):
        """Check program execute state"""

        if os.path.exists(self._pid_file):
            with open(self._pid_file, 'r') as f:
                self.pid = int(f.read())

            if self._process_is_running():
                logger.warning('Process is running, gracefully shutdown.')
                return True
            else:
                os.remove(self._pid_file)
                return False

        return False

    def _setup(self):
        if self._check_is_alive():
            raise SystemExit

        with open(self._pid_file, 'w') as f:
            f.write(str(os.getpid()))

    def _cleanup(self):
        if os.path.exists(self._pid_file):
            os.remove(self._pid_file)

        return None


if __name__ == '__main__':
    import time
    logging.basicConfig(level=logging.DEBUG)
    with ExclusvieWapper(__file__).exclusvie_check():
        try:
            for _ in range(20):
                time.sleep(1)
        except KeyboardInterrupt:
            logger.warning('Catch KeyboardInterrupt, shutdown test case.')
        except:
            raise
