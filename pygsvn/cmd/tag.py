# -*- coding: utf-8 -*-
from pygsvn import git

def execute(tag):
    '''
    add tag of git
    :param tag: name of tag
    '''
    return git.tag(tag)