import subprocess

def execute(path='.'):
    ''' show SVN and git logs '''
    subprocess.Popen('TortoiseProc /command:log /path:%s' % path)
    subprocess.Popen("tortoisegitproc /command:log /path:\"%s\"" % path)
