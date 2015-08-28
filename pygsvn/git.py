# -*- coding: utf-8 -*-
from pygsvn.cli import *
from pygsvn.util import *
import os

TAG_APPLY_DEBUG = 'APPLY-DEBUG'

def is_dirty():
    r = run_check_output('git status --porcelain') or ''
    files = [ x.strip().split(' ', 1) for x in r.split("\n") if x.strip() != '' ]
    return len(files) > 0

def get_status():
    r = run_check_output('git status --porcelain') or ''
    files = [ x.strip().split(' ', 1) for x in r.split("\n") if x.strip() != '' ]
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

def stash(msg='', check_dirty=True):
    if not check_dirty or is_dirty():
        # run('git stash save "%s"' % msg)
        old_branch = get_current_branch()
        import time
        msg = msg or "stash at " + time.strftime("%Y-%m-%d-%H:%M:%S")
        tag = 'stash-' + time.strftime("%Y%m%d-%H%M%S")
        run_check_return('git checkout -b "%s"' % tag)
        run_check_return('git add --all .')
        run_check_return('git commit -m "%s"' % msg)
        run_check_return('git checkout "%s"' % old_branch)
        return tag
    return ''

def pop_stash(tag):
    if tag:
        run_check_confirm(['git', 'merge', '--no-ff', tag])
        run_check_confirm(['git', 'branch', '-d', tag])


def tag(tag, commit=None):
    import os
    if exists_tag(tag):
        run('git tag -d "%s"' % tag)

    if commit == None:
        run('git tag "%s"' % tag)
    else:
        run('git tag "%s" "%s"' % (tag, commit))

def exists_tag(tag):
    tag_file = os.path.join(*('./.git/refs/tags/' + tag).split('/'))
    if os.path.isfile(tag_file):
        return True

    packed_refs_file = os.path.join(*'./.git/packed-refs'.split('/'))
    if os.path.isfile(packed_refs_file):
        packed_refs_file = open(packed_refs_file)
        with (packed_refs_file):
            for line in packed_refs_file:
                if line[0] == '#':
                    continue

                commit, ref = line.strip().split(' ', 1)
                if 'refs/tags/' + tag == ref:
                    return True

    return False


def mark_debug(commit=None):
    tag(TAG_APPLY_DEBUG, commit)

def revert_debug():
    return run_check_confirm('git revert --no-edit %s ' % TAG_APPLY_DEBUG)

def apply_debug():
    try:
        r = run_check_output('git cherry-pick %s ' % TAG_APPLY_DEBUG)
    except subprocess.CalledProcessError as e:
        if find_first_group_matches('(nothing to commit)', e.output):
            run('git cherry-pick --abort')

def get_log(options):
    r = run_check_output('git log --format="format:%h %s" ' + options)
    for line in r.split("\n"):
        line = line.strip()
        if line:
            sha, comment = line.split(' ', 1)
            yield {'sha': sha, 'comment': comment}


def try_commit(msg, dir='.'):
    try:
        run('git commit %s --message "%s"' % (dir, msg))
    except:
        pass

def has_conflicts(path='.'):
    r = run_check_output('git status --porcelain') or ''
    files = [ x.strip().split(' ', 1) for x in r.split("\n") if x.strip() != '' ]
    for status, file in files:
        if 'U' in status:
            return True
    return False