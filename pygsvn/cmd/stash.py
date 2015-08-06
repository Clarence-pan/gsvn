# -*- coding: utf-8 -*-
from pygsvn.cli import *
from pygsvn.util import *
from pygsvn import git

def execute(msg=''):
    '''
    stash current working
    :param msg: message for stash
    '''
    git.stash(msg)