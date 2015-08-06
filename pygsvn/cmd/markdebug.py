from pygsvn import git

name='mark-debug'

def execute(commit=None):
    '''mark specificied commit (or default current HEAD) as APPLY-DEBUG '''
    return git.mark_debug(commit)
