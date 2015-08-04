# -*- coding: utf-8 -*-
from pygsvn.cli import *
from pygsvn.util import *
from pygsvn import git

def execute(msg='', *args):
    '''
    stash current working
    :param msg: message for stash
    '''
    if git.is_dirty():
        run('git stash "%s"' % msg)