# -*- coding: utf-8 -*-
from pygsvn.cli import *
from pygsvn.util import *
from pygsvn import git, svn
from pygsvn.cmd import tsvn, update, Option
import os, json
STATE_FILE = os.path.join(*('./.git/.gsvn-store'.split('/')))

aliases = ('c', 'co')
options = (
    Option('isContinue', ('c', 'continue'), desc='is to continue previous commitment'),
    Option('needConfirm', ('y', 'confirm'), desc='need confirm or not before commit to SVN'),
    Option('msg', ('m', 'message'), type='string', required=True, desc='message of commitment')
)

def execute(msg, isContinue=False, needConfirm=False):
    ''' commit changes of working '''
    try:
        if not msg and not isContinue:
            print 'Error: please specify the message of commit.'
            return 1

        if not isContinue:
            if git.is_dirty():
                print 'Error: dirty working directory! Please stash or commit local changes to git.'
                return 1
            git.revert_debug()
        else:
            state = load_state()
            if not state or state['state'] != 'commit':
                print "Error: invalid state!"
                return 1

        if needConfirm:
            tsvn.execute('commit')
        else:
            # run('svn commit --message "%s"' % msg)
            svn.commit(msg)

        git.tag('COMMITED')
        update.execute(True)
        git.apply_debug()
    except Exception, e:
        print "Error: commit failed! Please solve the conflicts and use 'gsvn commit --continue' to go on."
        print e
        raise

def save_state(data):
    file_put_contents(json.dumps(data))

def load_state():
    text = file_get_contents(STATE_FILE)
    return json.loads(text)