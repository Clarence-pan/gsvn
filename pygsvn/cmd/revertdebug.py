__author__ = 'panchangyun'

from pygsvn import git

def execute():
    '''
    revert debug codes
    '''
    return git.revert_debug()