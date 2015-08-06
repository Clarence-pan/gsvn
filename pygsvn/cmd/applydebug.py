from pygsvn import git

name = 'apply-debug'
aliases = ('redebug', 'ad')

def execute():
    ''' apply debug codes '''
    return git.apply_debug()