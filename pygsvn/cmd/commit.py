# -*- coding: utf-8 -*-
from pygsvn.cli import *
from pygsvn.util import *
from pygsvn import git, svn
from pygsvn.cmd import tsvn, update, Option
import os, json
STATE_FILE = os.path.join(*('./.git/.gsvn-store'.split('/')))

aliases = ('c', 'co')
options = (
    Option('needConfirm', ('c', 'y', 'confirm'), desc='need confirm or not before commit to SVN'),
    Option('msg', ('m', 'message'), type='string', required=False, desc='message of commitment')
)

def execute(msg='', needConfirm=False):
    ''' commit changes of working '''
    try:
        if not msg and not needConfirm:
            print 'Error: please specify the message of commit.'
            return 1

        if git.is_dirty():
            print 'Error: dirty working directory! Please stash or commit local changes to git.'
            return 1

        initial_branch = git.checkout_branch('svn')
        run_check_confirm('git checkout -b commiting')
        git.revert_debug()

        if needConfirm:
            tsvn.execute('commit')
            if git.is_dirty():
                run_check_confirm('git add --all .')
                run_check_confirm(['git', 'commit', '-m', 'auto commit after commit to svn'])
        else:
            # run('svn commit --message "%s"' % msg)
            svn.commit(msg)

        git.tag('COMMITED')
        #update.execute(True)
        git.apply_debug()
        run_check_confirm('git checkout svn')
        run_check_confirm('git merge commiting --no-ff')
        run_check_confirm('git branch -d commiting')
        git.checkout_branch(initial_branch)
    except Exception, e:
        print "Error: commit failed! Please solve the conflicts and use 'gsvn commit --continue' to go on."
        print e
        raise

def save_state(data):
    file_put_contents(json.dumps(data))

def load_state():
    text = file_get_contents(STATE_FILE)
    return json.loads(text)