from pygsvn import git
from pygsvn.cli import *
from pygsvn.cmd import Option

aliases = ('v', 'va')
options = (
    Option('nostash', ('n', 'no-stash'), desc='not to stash before update'),
)

def execute(nostash=True):
    ''' validate it '''
    if not nostash:
        git.stash('before validate')

    initial_branch = git.checkout_branch('svn', returnOld=True)
    r = run_check_output('svn status')
    if r.strip() != "":
        print "Error: svn and work do NOT match! "
        return 1
    else:
        print "It's OK"
        git.checkout_branch(initial_branch, returnOld=False)
        return  0
