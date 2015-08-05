from pygsvn import git,svn

def execute(path='.', *args):
    '''
    resolve SVN and git conflicts
    :param path:
    '''
    if svn.has_conflicts(path):
        from pygsvn.cmd import tsvn
        tsvn.execute('resolve')

    if git.has_conflicts(path):
        from pygsvn.cmd import tgit
        tgit.execute('resolve')
