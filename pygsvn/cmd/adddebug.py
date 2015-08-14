from pygsvn import git, svn
from pygsvn.util import *
from pygsvn.cli import *

name = 'add-debug'

def execute(commit='HEAD'):
    '''
    add debug code of some commit
    '''
    git.stash()
    run_check_confirm('git revert %s --no-commit' % commit)
    run_check_confirm('git revert %s --no-commit' % git.TAG_APPLY_DEBUG)
    run_check_confirm('git add --all .'.split(' '))
    run_check_confirm(['git', 'commit', '-m', "revert all debug code"])
    run_check_confirm('git revert HEAD --no-edit --no-commit')
    run_check_confirm('git commit -m "debug: add debug code"')
    git.tag(git.TAG_APPLY_DEBUG)

