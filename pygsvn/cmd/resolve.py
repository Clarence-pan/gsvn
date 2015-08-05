from pygsvn import git,svn

def execute(path='.', *args):
    if svn.has_conflicts(path):
        from pygsvn.cmd import tsvn
        tsvn.execute('resolve')

    if git.has_conflicts(path):
        from pygsvn.cmd import tgit
        tgit.execute('resolve')
