# -*- coding: utf-8 -*-
from pygsvn.cli import *
from pygsvn.cmd import tgit

aliases = ('ts',)
options = tgit.options

def execute(cmd, path='.'):
    """ execute tortoise SVN """
    return run_check_confirm(['TortoiseProc', '/command:%s' % cmd, '/path:%s' % path])