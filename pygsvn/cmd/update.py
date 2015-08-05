# -*- coding: utf-8 -*-
import os
from pygsvn.cli import *
from pygsvn.util import *
from pygsvn import git, svn

def execute(nostash=False, *args):
    '''
    update current workspace form SVN
    :param nostash: do not stash
    '''
    initial = git.get_status()
    if initial['isDirty']:
        if not nostash:
            git.stash('before update', check_dirty=False)

    if initial['branch'] != 'svn':
        run_check_return('git checkout svn')

    run('svn update --accept postpone')

    if svn.has_conflicts():
        print "There are some SVN conflicts, please resolve before continue."
        from pygsvn.cmd import tsvn
        tsvn.execute('resolve')

    r = run_check_output('svn info')
    revision = find_first_group_matches(r'Revision:\s(\d+)', r)

    status = git.get_status()
    if status['files']:
        run_check_return('git add --all .')
        run_check_return('git commit . -m "update to svn(r%s)"' % revision)

    git.tag('UPDATE-TO-r%s' % revision)

    if initial['branch'] != 'svn':
        run_check_return('git checkout "%s"' % initial['branch'])
        run_check_return('git merge svn')
