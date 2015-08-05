# -*- coding: utf-8 -*-
import subprocess

def execute(path='.', *args):
    """
    execute tortoise SVN
    :param path [optional] default is '.'
    """
    return subprocess.Popen("TortoiseProc /command:log /path:%s" % path)