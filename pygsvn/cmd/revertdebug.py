__author__ = 'panchangyun'

from pygsvn import git

name = 'revert-debug'
aliases = ('undebug', 'udbg', 'ud')

def execute():
    ''' revert debug codes '''
    return git.revert_debug()