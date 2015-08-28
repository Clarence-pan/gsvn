# -*- coding: utf-8 -*-
import os
from pygsvn.cli import *
from pygsvn.util import *
from pygsvn import git, svn
from pygsvn.cmd import Option

options = (
    Option('nostash', ('n', 'no-stash'), desc='not to stash before update'),
)

def execute(nostash=False):
    ''' update current workspace form SVN '''
    initial = git.get_status()
    stash_tag = ''
    if initial['isDirty']:
        if not nostash:
            stash_tag = git.stash('before update', check_dirty=False)

    if initial['branch'] != 'svn':
        run_check_confirm(['git', 'checkout', 'svn'])

    update_output = run_check_output('svn update --accept postpone .')

    if svn.has_conflicts():
        print "There are some SVN conflicts, please resolve before continue."
        from pygsvn.cmd import tsvn
        tsvn.execute('resolve')

    r = run_check_output('svn info')
    revision = find_first_group_matches(r'Revision:\s(\d+)', r)

    status = git.get_status()
    if status['files']:
        run_check_confirm('git add --all .')
        run_check_confirm(['git', 'commit', '.', '-m', "update to svn(r%s)" % revision])

    #git.tag('UPDATE-TO-r%s' % revision)

    if initial['branch'] != 'svn':
        run_check_confirm(['git', 'checkout', initial['branch']])
        run_check_confirm(['git', 'merge', '--no-ff', 'svn'])

    if stash_tag:
        git.pop_stash(stash_tag)

    print
    print "--- Updated ---"
    print update_output
