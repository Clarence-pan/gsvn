# -*- coding: utf-8 -*-
import os

name='tsvn-diff'

def execute(path='.'):
    """ execute tortoise SVN """
    return os.system("TortoiseProc /command:diff /path:%s" % path)