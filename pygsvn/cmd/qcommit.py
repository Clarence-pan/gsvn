from pygsvn.cmd import commit, Option
from pygsvn.cli import *
from pygsvn import git

options = (
    Option('isContinue', ('c', 'continue')),
    Option('needConfirm', ('y', 'confirm')),
)

def execute(msg=None, isContinue=False, needConfirm=False):
    '''
    commit to git and svn
    :param msg - the log message
    '''
    if not msg:
        print 'Error: commit message must not be empty!'
        sys.exit(1)

    run('git status')
    run('git add --all .')
    git.try_commit(msg)
    commit.execute(msg)
