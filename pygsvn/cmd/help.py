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
            print " ", cmd_obj.get_cmd_form()
            if cmd_obj.aliases:
                print
                print "  alias:", ' '.join(cmd_obj.aliases)
            print
            print ' ', cmd_obj.get_doc().lstrip()
    else:
        print "About gsvn:"
        print "      gsvn  - a tool to make svn works with git!"
        print
        print "Commands:"

        for cmd_obj in get_all_cmds():
            print "  %-15s - %s" % (cmd_obj.full_name, cmd_obj.get_desc())
