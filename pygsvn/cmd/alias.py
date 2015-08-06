from pygsvn.cmd import help

def execute(alias=None):
    '''
    there are many aliases, this command show the aliases
    :param alias: which alias to display
    '''
    if alias == None:
        for full_cmd, aliases in help.get_all_alias().items():
            print "%-15s  %s" % (full_cmd, ', '.join(aliases))
    else:
        full_cmd = help.get_cmd_from_alias(alias)
        print "%s = %s" % (alias, full_cmd)