#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os

import utils


class TestFopen(object):
    fname = 'test.txt'
    mode = 'w'

    def teardown_method(self, method):
        try:
            os.remove(self.fname)
        except OSError:
            pass

    def test_case1(self):
        with utils.Fopen(self.fname, self.mode):
            raise SystemExit

        assert os.path.isfile(self.fname) == False

    def test_case2(self):
        with utils.Fopen(self.fname, self.mode):
            pass

        assert os.path.isfile(self.fname) == True


class TestLockFile(object):
    pass
