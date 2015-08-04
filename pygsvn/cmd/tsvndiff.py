# -*- coding: utf-8 -*-
import os

def execute(path='.', *args):
    """
    execute tortoise SVN
    :param path [optional] default is '.'
    """
    return os.system("TortoiseProc /command:diff /path:%s" % path)