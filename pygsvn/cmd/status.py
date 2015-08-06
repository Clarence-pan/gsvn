from pygsvn.cli import *

aliases = ('st',)

def execute():
    ''' show current workcopy status '''
    run('svn status')
    run('git status')
