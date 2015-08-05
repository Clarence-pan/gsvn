# -*- coding: utf-8 -*-
import os
from pygsvn.cli import *
from pygsvn.util import *

def execute(url, path='.', *args):
    '''
    init a repo
    '''
    run('svn checkout "%s" "%s"' % (url, path))
    run('git init "%s"' % path)
    file_put_contents(os.path.join(path, '.gitignore'), "\n".join(['.svn/', '.bak', '~']))
    run('git config core.autocrlf false')
    os.chdir(path)
    run('git add --all .')
    output = run_check_output('svn info')
    revision = find_first_group_matches(r'Revision:\s(\d+)', output)
    run('git commit -m "initialized from svn(r%s)"' % revision)
    run('git checkout -b svn')
    run('git checkout -b debug')
    print 'Initialization done. Enjoy yourself!'