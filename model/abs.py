#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class NonOverrideable(type):

    def __new__(cls, name, bases, attr):
        if bases and "update" in attr:
            raise SyntaxError("Method update can't be overrided.")

        return super(NonOverrideable, cls).__new__(cls, name, bases, attr)


class AbsLogger(object):

    def get_logger(self):
        raise NotImplementedError


class AbsApp(object):

    __metaclass__ = NonOverrideable

    def __init__(self):
        self._logger = AbsLogger()

    def upstall(self):
        self._upstall()

    def _upstall(self):
        if self._exist():
            self._update()
            self._backup()
        else:
            self._restore()
            self._install()

    def _update(self):
        raise NotImplementedError

    def _backup(self):
        raise NotImplementedError

    def _restore(self):
        raise NotImplementedError

    def _install(self):
        raise NotImplementedError


class AbsFactory(object):

    def create_app(self):
        raise NotImplementedError

    def create_logger(self):
        raise NotImplementedError
