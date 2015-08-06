# -*- coding: utf-8 -*-

from pygsvn.cmd import *

aliases = ('?', 'h', 'help')

def execute(cmd=None, *args):
    """simple help about gsvn"""
    if cmd != None:
        cmd_obj = get_cmd(cmd)
        if cmd_obj == None:
            print "Unknown command '%s'." % cmd
        else:
            print "About `%s`: " % cmd
            print "Full command: ", cmd_obj.full_name
            print "Alias: ", ' '.join(cmd_obj.aliases)
            print ' ', get_cmd_doc(cmd).lstrip().capitalize()
    else:
        print "About gsvn:"
        print "      gsvn  - a tool to make svn works with git!"
        print
        print "Commands:"

        for cmd_obj in get_all_cmds():
            print "  %-15s - %s" % (cmd_obj.full_name, cmd_obj.get_desc)
