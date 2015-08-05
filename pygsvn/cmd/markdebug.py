from pygsvn import git

def execute(commit=None, *args):
    '''
    mark specificied commit (or default current HEAD) as APPLY-DEBUG
    '''
    return git.mark_debug(commit)
