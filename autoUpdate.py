#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import logging
import os
import argparse
import weakref
import subprocess as sp

import pip

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


pip_update_cmd = '/usr/local/var/pyenv/shims/pip install -U'

PipOutputIgnoreCmd = 'grep -v up-to-date'

VimUpdateCmd = ''


# TODO vim Plugin upate
# TODO logrotate


class TargetMetaClass(type):

    # TODO: wrapper a new attr for read out of class
    _obj_dict = weakref.WeakValueDictionary()
    _log_dict = {}

    def target_dict(self, key):
        return self._obj_dict[key]

    def __new__(cls, name, bases, attr):

        raw_name = name.lower()
        newcls = super(TargetMetaClass, cls).__new__(cls, name, bases, attr)
        cls._obj_register(raw_name, newcls)
        cls._log_register(raw_name)
        return newcls

    @classmethod
    def _obj_register(cls, name, obj):
        """Register subclass to dict."""

        cls._obj_dict[name] = obj

    @classmethod
    def _log_register(cls, name):
        log_file = cls._convert(name)
        cls._log_dict[name] = log_file

    @classmethod
    def _convert(cls, cls_name):
        """From class name generate a log file location."""

        log_dir = os.getenv('HOME') + '/AutoUpdateLog'
        if not os.path.exists(log_dir):
            os.mkdir(log_dir, 0755)
        log_file = log_dir + '/{}.log'.format(cls_name)

        return log_file


class TargetVC(object):

    __metaclass__ = TargetMetaClass

    def __init__(self):
        self.location = TargetVC.locate_traget(self.__class__.__name__.lower())

    @staticmethod
    def locate_traget(target):
        cmd = 'which' + ' ' + target
        try:
            re = sp.check_output(cmd.split())
        except sp.CalledProcessError:
            cmd = 'find /bin /sbin /usr/sbin /usr/local/bin /opt \
                  /etc/opt /var/opt -executable -type f -name {} \
                  | head -n 1'.format(target)
            re = sp.check_output()
            pass
        return re
        # 1.use call which target
        # 2.use find target
        # 3.else raise a error
        # return

    def update(self):
        raise NotImplementedError

    @staticmethod
    def create(target):
        try:
            return TargetVC.target_dict(target)
        except KeyError:
            logger.warning('Target does not resigter, plz check out')


class Brew(TargetVC):

    _cmd_list = ('upgrade', 'cleanup')

    def update(self):
        [sp.call((self.location + ' ' + cmd).split()) for cmd in self._cmd_list]


class Pip(TargetVC):
    """Class which used to update pip"""


class Vim(TargetVC):
    """Class which used to update vim"""


def pip_update():
    integrate_update()
    reload(pip)
    for dist in pip.get_installed_distributions():
        integrate_update(dist.project_name)


def integrate_update(cmd='pip'):
    new_cmd = pip_update_cmd + ' ' + cmd
    sp.call(new_cmd.split(), stdout=file, stderr=file)
    p = sp.Popen(new_cmd.split(), stdout=sp.PIPE, stderr=sp.PIPE)
    sp.call(
        PipOutputIgnoreCmd.split(),
        stdin=p.stdout,
        stdout=file,
        stderr=file)
    p.wait()


def main():
    parser = argparse.ArgumentParser('Auto update script for tools')
    parser.add_argument(
        dest='updateName',
        help='Please input what kind of tools you wanna update:\n \
        brew/pip/vim')
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Open debug mode',
        default=False)

    args = parser.parse_args()

    if args.debug:
        log_lvl = logging.DEBUG
    else:
        log_lvl = logging.INFO

    try:
        pass
        # value = _functions[args.updateName]
    except KeyError:
        parser.print_help()
        return False

    logging.basicConfig(
        level=log_lvl,
        filename=value[1],
        format='%(asctime)s %(levelname)s %(filename)s \
                %(lineno)d %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    value[0]()


if __name__ == '__main__':
    main()
