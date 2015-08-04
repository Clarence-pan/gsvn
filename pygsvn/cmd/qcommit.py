from pygsvn.cmd import commit
from pygsvn.cli import *
from pygsvn import git

def execute(msg, *args, **kwargs):
    '''
    commit to git and svn
    :param msg - the log message
    '''
    run('git status')
    run('git add .')
    git.try_commit(msg)
    commit.execute(msg, **kwargs)
