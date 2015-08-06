from pygsvn.cli import *

def execute():
    '''
    show current workcopy status
    '''
    run('svn status')
    run('git status')
