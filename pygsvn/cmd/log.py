import subprocess

def execute(path='.', *args):
    '''
    show SVN and git logs
    '''
    subprocess.Popen('TortoiseProc /command:log /path:%s' % path)
    subprocess.Popen("tortoisegitproc /command:log /path:\"%s\"" % path)
