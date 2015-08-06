# -*- coding: utf-8 -*-
import os
from pygsvn.cmd import Option

aliases = ('tg', )
options = (
    Option('cmd', ('c', 'e', 'command', 'execute'), type='string', required=True, desc='command to execute'),
    Option('path', ('p',), type='string', desc='path to execute command')
)

def execute(cmd, path='.'):
    """ execute tortoise git """
    return os.system("tortoisegitproc /command:%s /path:\"%s\"" % (cmd, path))