from pygsvn.cli import *
from pygsvn.util import *
import os
from pygsvn import git

def has_conflicts(path='.'):
    stat = get_status_summary(path)
    return '!' in stat or 'C' in stat

def commit(msg, path='.'):
    if not msg:
        raise ValueError('msg must not empty when committing')

    stat = get_status_summary()
    if '?' in stat or '!' in stat or 'C' in stat:
        print "you must resolve conflicts and add unversion files before commit"
        from pygsvn.cmd import tsvn
        tsvn.execute('diff', path)

    run_check_return('svn commit %s --message "%s"' % (path, msg))

def get_status_summary(path='.'):
    stat = get_status(path)
    summary = []
    for file_stat in stat.keys():
        for one_stat in file_stat:
            if one_stat not in summary:
                summary.append(one_stat)
    return summary

def get_status(path='.'):
    r = run_check_output('svn status "%s"' % path)
    files = [(x[:7], x[8:].strip()) for x in r.strip().split("\n") if x.strip() != '']
    status_files = {}
    for status, file in files:
        if file and os.path.exists(file):
            if not status in status_files:
                status_files[status] = [file]
            else:
                status_files[status].append(file)
    return status_files

def get_unversioned_files(path='.'):
    r = run_check_output(['svn', 'status', path])
    return [x[8:].strip() for x in r.strip().split("\n") if x.strip() != '' and x[0] == '?']

def remove_all_unversioned_files(path='.'):
    unversioned_files = get_unversioned_files(path)
    for f in unversioned_files:
        if os.path.isdir(f):
            run_check_confirm(['rm', '-rf', f])
        else:
            run_check_confirm(['rm', '-f', f])