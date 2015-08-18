# -*- coding: utf-8 -*-
import os

name='tsvn-diff'

def execute(path='.'):
    """ execute tortoise SVN modification/difference"""
    return os.system("TortoiseProc /command:diff /path:%s" % path)