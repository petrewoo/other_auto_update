#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import logging

from .abs import *

logger = logging.getLogger(__name__)


class VimLogger(AbsLogger):
    pass


class Vim(AbsApp):

    def __init__(self):
        self._logger = VimLogger()

    def _exist(self):
        pass

    def _update(self):
        pass

    def _backup(self):
        pass

    def _restore(self):
        pass


class VimFactory(AbsFactory):

    @staticmethod
    def create_app():
        return Vim()
