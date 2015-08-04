# -*- coding: utf-8 -*-
import os

def execute(cmd, path='.', *args):
    """
    execute tortoise SVN
    :param cmd
    :param path [optional] default is '.'
    """
    return os.system("TortoiseProc /command:%s /path:%s" % (cmd, path))