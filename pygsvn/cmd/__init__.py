# -*- coding: utf-8 -*-
import glob, os
from pygsvn.util import *

def get_all_cmds():
    cmd_dir, _ = os.path.split(__file__)
    for filepath in glob.glob(os.path.join(cmd_dir, '*.py')):
        _, filename = os.path.split(filepath)
        basename, extname = os.path.splitext(filename)
        if basename != '__init__':
            yield (basename, get_cmd_desc(basename))

def get_cmd(cmd):
    try:
        cmd = get_cmd_from_alias(cmd)
        parent_mod = __import__('pygsvn.cmd.'+cmd)
        cmd_mod = getattr(parent_mod, 'cmd')
        return getattr(cmd_mod, cmd)
    except ImportError:
        return None

def get_cmd_doc(cmd):
    return get_cmd(cmd).execute.__doc__ or cmd

def get_cmd_desc(cmd):
    doc = get_cmd_doc(cmd)
    lines = doc.split("\n")
    for line in lines:
        line = line.strip()
        if line != '':
            return line

def get_cmd_from_alias(alias):
    alias = alias.replace('/','').replace('-','')
    all_alias = get_all_alias()
    for full_cmd, aliases in all_alias.items():
        if alias in aliases:
            return full_cmd
    return alias

def get_all_alias():
    return {
        'help': ('?', 'h', 'help'),
        'qcommit': ("qc", 'qco'),
        'commit': ('c', 'co'),
        'tsvn': ('ts',),
        'tgit': ('tg',),
        'validate': ('v', 'va'),
        'revertdebug': ('undebug', 'udbg', 'ud'),
        'applydebug': ('apply-debug', 'redebug', 'ad'),
        'status': ('st',)
    }
