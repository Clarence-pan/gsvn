# -*- coding: utf-8 -*-
import os
from pygsvn.cmd import stash
from pygsvn.cli import *
from pygsvn.util import *
from pygsvn import git

def execute(nostash=False, *args):
    '''
    update current workspace form SVN
    :param nostash: do not stash
    '''
    initial = git.get_status()
    if initial['isDirty']:
        if not nostash:
            stash.execute('before update')

    if initial['branch'] != 'svn':
        run('git checkout svn')

    run('svn update --accept postpone')

    gstatus = git.get_status()
    if has_svn_conflict(gstatus['files']):
        print "There are some SVN conflicts, please resolve before continue."
        from pygsvn.cmd import tsvn
        tsvn.execute('resolve')

    r = run_check_output('svn info')
    revision = find_first_group_matches(r'Revision:\s(\d+)', r)
    run('git add .')
    git.try_commit('update to svn(r%s)' % revision)
    git.tag('UPDATE-TO-r%s' % revision)

    if initial['branch'] != 'svn':
        run('git checkout "%s"' % initial['branch'])
        run('git merge svn')

def has_svn_conflict(files):
    for status, filepath in files:
        _, ext = os.path.splitext(filepath)
        if ext == '.mine':
            return True
    return False