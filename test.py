#!/usr/bin/env python

from pygsvn.cmd import *
from pygsvn.cli import *


if __name__ == '__main__':
    print 'python ./gsvn.py help'
    for cmd in get_all_cmds():
        print "python ./gsvn.py %s -h" % cmd.full_name
