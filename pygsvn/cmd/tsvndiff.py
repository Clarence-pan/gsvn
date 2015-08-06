# -*- coding: utf-8 -*-
import os

def execute(path='.'):
    """
    execute tortoise SVN
    :param path [optional] default is '.'
    """
    return os.system("TortoiseProc /command:diff /path:%s" % path)