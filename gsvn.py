#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pygsvn.cmd

def main(argv):
    if len(argv) <= 1:
        cmd = 'help'
        args = []
    else:
        cmd = argv[1]
        args = argv[2:]

    cmd_executor = pygsvn.cmd.get_cmd(cmd)
    if cmd_executor == None:
        print "Error: Unknown cmd '%s'!" % cmd
        return 1

    return cmd_executor.execute(*args)

if __name__ == '__main__':
    sys.exit(main(sys.argv))