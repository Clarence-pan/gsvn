from pygsvn.cli import *

def execute(*args):
    '''
    see the info of current path
    '''
    run('svn info')