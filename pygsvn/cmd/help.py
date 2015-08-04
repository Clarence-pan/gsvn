# -*- coding: utf-8 -*-

from pygsvn.cmd import *

def execute(cmd=None, *args):
    """simple help about gsvn"""
    if cmd != None:
        cmd_obj = get_cmd(cmd)
        if cmd_obj == None:
            print "Unknown command '%s'." % cmd
        else:
            print "About `%s`: " % cmd
            print get_cmd_doc(cmd)
    else:
        print "About gsvn:"
        print "      gsvn  - a tool to make svn works with git!"
        print
        print "Commands:"

        for name, desc in get_all_cmds():
            print "  %-10s - %s" % (name, desc)
