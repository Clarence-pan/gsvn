from pygsvn import git
from pygsvn.cli import *
from pygsvn.util import *

def execute():
    '''
    make debug from SVN changes
    '''
    git.stash('before make-debug')
    run_check_return('svn revert -R .')
    run_check_return('git add .')
    r = run_check_output('git commit . -m "revert-debug"')
    commit = find_first_group_matches('\[.+\s+(.*)\]', r)
    if not commit:
        print "Error: No commit found!"
        return 1

    run_check_return('git revert --no-edit --no-commit %s' % commit)
    run_check_return('git commit --message "apply-debug(by make-debug)" .')
    git.mark_debug()

