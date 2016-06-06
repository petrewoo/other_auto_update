#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from subprocess import call, Popen, PIPE, STDOUT
import datetime
import os
import argparse
import pip


# TODO vim Plugin upate
BrewUpdateCmdList = [("/usr/local/bin/brew", "update"),
                     ("/bin/rm", "/usr/local/bin/vim"),
                     ("/usr/local/bin/brew", "upgrade"),
                     ("/bin/ln", "-sf", "/usr/local/bin/mvim",
                      "/usr/local/bin/vim"),
                     ("/usr/local/bin/brew", "cleanup")]
PipUpdateBaseCmd = ("pip", "install", "-U")
PipOutputIgnoreCmd = ("grep", "-v", "up-to-date")

home = os.getenv("HOME")
BREWLOG = home + "/log/cronTaskBrewUpdate.log"
PIPLOG = home + "/log/cronTaskPipUpdate.log"


def brew_update():
    with open(BREWLOG, "a") as f:
        _block_area(f)
        _time_stamp(f)
        for cmd in BrewUpdateCmdList:
            call(cmd, stdout=f, stderr=f)
        _block_area(f)


def pip_update():
    with open(PIPLOG, "a") as f:
        _block_area(f)
        _time_stamp(f)
        _integrate_update(f)
        reload(pip)
        for dist in pip.get_installed_distributions():
            _integrate_update(f, dist.project_name)
        _block_area(f)


def _combine(cmd='pip'):
    return PipUpdateBaseCmd + (cmd,)


def _integrate_update(file, cmd='pip'):
    new_cmd = PipUpdateBaseCmd + (cmd,)
    p = Popen(new_cmd, stdout=PIPE, stderr=STDOUT)
    call(PipOutputIgnoreCmd, stdin=p.stdout, stdout=file, stderr=file)
    p.wait()


def _block_area(file):
    file.write("*" * 80 + "\n")
    file.flush()


def _time_stamp(file):
    now = datetime.datetime.now()
    file.write(now.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    file.flush()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('updateName', help='plz input your what kind of tools you wanna update, \
                        1:bv(brew&vim) 2:pip')
    args = parser.parse_args()
    if args.updateName == 'bv':
        brew_update()
    elif args.updateName == 'pip':
        pip_update()
    else:
        parser.print_help()
