# -*- coding: utf-8 -*-
import os
from pygsvn.cmd import tgit

aliases = ('ts',)
options = tgit.options

def execute(cmd, path='.'):
    """ execute tortoise SVN """
    return os.system("TortoiseProc /command:%s /path:%s" % (cmd, path))