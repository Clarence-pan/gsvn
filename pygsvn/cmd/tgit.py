# -*- coding: utf-8 -*-
import os

def execute(cmd, path='.'):
    """
    execute tortoise git
    :param cmd
    :param path [optional] default is '.'
    """
    return os.system("tortoisegitproc /command:%s /path:\"%s\"" % (cmd, path))