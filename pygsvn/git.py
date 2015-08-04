# -*- coding: utf-8 -*-
from pygsvn.cli import *
from pygsvn.util import *
import os

def is_dirty():
    r = run_check_output('git status')
    return not str_contains('nothing to commit', r.split("\n")[1])

def get_status():
    r = run_check_output('git status --porcelain')
    files = [ str_split2(x.strip()) for x in r.split("\n") if x.strip() != '' ]
    return {
        'branch' : get_current_branch(),
        'isDirty': len(files) > 0,
        'files': files
    }

def get_current_branch():
    # r = run_check_output('git status')
    # return find_first_group_matches(r'On branch (\w+)', r)
    head = file_get_contents(os.path.join('.git', 'HEAD'))
    return find_first_group_matches(r"ref: refs/heads/(.*)\S*", head)

def checkout_branch(branch, returnOld=False):
    initial_branch = get_current_branch()
    if initial_branch != branch:
        run('git checkout "%s"' % branch)
    return initial_branch

def tag(tag):
    import os
    if os.path.isfile(os.path.join('.', '.git', 'refs', 'tags', tag)):
        run('git tag -d "%s"' % tag)
    run('git tag "%s"' % tag)

def revert_debug():
    return run('git cherry-pick REVERT-DEBUG')

def apply_debug():
    return run('git cherry-pick APPLY-DEBUG')

def get_log(options):
    r = run_check_output('git log --format="format:%h %s" ' + options)
    for line in r.split("\n"):
        line = line.strip()
        if line:
            sha, comment = str_split2(line)
            yield {'sha': sha, 'comment': comment}


def try_commit(msg, dir='.'):
    try:
        run('git commit %s --message "%s"' % (dir, msg))
    except:
        pass