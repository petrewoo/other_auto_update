#!/usr/bin/env python
# encoding: utf-8

from subprocess import call
import datetime
import os
import argparse
import pip

# TODO vim Plugin upate

brewUpdateCmdList = [("/usr/local/bin/brew", "update"),
                     ("/bin/rm", "/usr/local/bin/vim"),
                     ("/usr/local/bin/brew", "upgrade"),
                     ("cp", "-R", "/usr/local/bin/vim.bk",
                      "/usr/local/bin/vim"),
                     ("/usr/local/bin/brew", "cleanup")]
pipUpdateCmdList = ["pip", "install", "-U"]

home = os.getenv("HOME")
BREWLOG = home + "/log/cronTaskBrewUpdate.log"
PIPLOG = home + "/log/cronTaskPipUpdate.log"


def brewUpdate():
    with open(BREWLOG, "a") as f:
        _blockArea(f)
        _timeStamp(f)
        for cmd in brewUpdateCmdList:
            call(cmd, stdout=f, stderr=f)
        _blockArea(f)


def pipUpdate():
    with open(PIPLOG, "a") as f:
        _blockArea(f)
        _timeStamp(f)
        call("pip install -U pip", shell=True)
        reload(pip)
        for dist in pip.get_installed_distributions():
            call("pip install -U " + dist.project_name, shell=True)
        _blockArea(f)


def _blockArea(file):
    file.write("*" * 80 + "\n")
    file.flush()


def _timeStamp(file):
    now = datetime.datetime.now()
    file.write(now.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    file.flush()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('updateName', help='plz input your what kind of tools you wanna update, \
                        1:bv(brew&vim) 2:pip')
    args = parser.args()
    if args.update == 'bv':
        brewUpdate()
    elif args.update == 'pip':
        pipUpdate()
    else:
        parser.print_help()
