#!/usr/bin/env python

from pygsvn.cmd import *
from pygsvn.cli import *
import os


if __name__ == '__main__':
    dir, _ = os.path.split(__file__)
    os.chdir(dir)
    run('python ./gsvn.py help')
    for cmd in get_all_cmds():
        run("python ./gsvn.py %s -h" % cmd.full_name)
