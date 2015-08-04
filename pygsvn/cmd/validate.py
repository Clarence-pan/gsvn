from pygsvn import git
from pygsvn.cmd import stash
from pygsvn.cli import *

def execute(nostash=True, *args):
    '''
    validate it
    :param nostash: - don't stash, just update it!
    '''
    if not nostash:
        stash.execute('before validate')

    initial_branch = git.checkout_branch('svn', returnOld=True)
    r = run_check_output('svn status')
    if r.strip() != "":
        print "Error: svn and work do NOT match! "
        return 1
    else:
        print "It's OK"
        git.checkout_branch(initial_branch, returnOld=False)
        return  0
