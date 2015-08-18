# -*- coding: utf-8 -*-
import subprocess

name = 'tsvn-log'

def execute(path='.'):
    """ execute tortoise SVN log """
    return subprocess.Popen("TortoiseProc /command:log /path:%s" % path)