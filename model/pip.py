#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import logging

from .abs import *

logger = logging.getLogger(__name__)


class PipLogger(AbsLogger):
    pass


class Pip(AbsApp):

    def __init__(self):
        self._logger = PipLogger()

    def _exist(self):
        pass

    def _update(self):
        pass

    def _backup(self):
        pass

    def _restore(self):
        pass


class PipFactroy(AbsFactory):

    @staticmethod
    def create_app():
        return Pip()
