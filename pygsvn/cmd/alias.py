from pygsvn.cmd import Option
from pygsvn.cmd import *

options = (
    Option('alias', ('a', 'name'), type='string', desc='name of which alias to show'),
)

def execute(alias=None):
    '''there are many aliases, this command show the aliases '''
    if alias == None:
        for cmd in get_all_cmds():
            print "%-15s  %s" % (cmd.full_name, ', '.join(cmd.aliases))
    else:
        full_cmd = get_cmd_from_alias(alias)
        if not full_cmd:
            print "Error: cannot find command for", alias
        print "%s = %s" % (alias, full_cmd.full_name)
        print "other aliases:", ', '.join(full_cmd.aliases)