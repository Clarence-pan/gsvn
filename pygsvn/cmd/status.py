from pygsvn.cli import *

def execute(*args):
    '''
    show current workcopy status
    '''
    run('svn status')
    run('git status')
