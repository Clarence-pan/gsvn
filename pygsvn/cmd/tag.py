# -*- coding: utf-8 -*-
from pygsvn import git
from pygsvn.cmd import Option

options = (
    Option('tag', ('t', 'n', 'name'), type='string', desc='name of the tag'),
)

def execute(tag):
    ''' add tag of git '''
    return git.tag(tag)