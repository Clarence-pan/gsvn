from pygsvn import git,svn

def execute(path='.'):
    ''' resolve SVN and git conflicts '''
    if svn.has_conflicts(path):
        from pygsvn.cmd import tsvn
        tsvn.execute('resolve')

    if git.has_conflicts(path):
        from pygsvn.cmd import tgit
        tgit.execute('resolve')
