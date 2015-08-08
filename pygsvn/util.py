# -*- coding: utf-8 -*-
import re

def find_first_group_matches(pattern, context):
    matches = re.search(pattern, context, re.MULTILINE)
    if matches != None:
        return matches.group(1)
    else:
        return ''


def file_put_contents(filepath, contents):
    f = open(filepath, 'wt')
    with(f):
        f.write(contents)

def file_get_contents(filepath):
    f = open(filepath, 'rt')
    with(f):
        return f.read()

