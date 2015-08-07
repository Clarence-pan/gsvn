#!/usr/bin/env python

from pygsvn.cmd import *
from pygsvn.cli import *
import os, unittest


def gsvn(args):
    return run('python ./gsvn.py ' + args)

class HelpTest(unittest.TestCase):
    def testHelpIteself(self):
        "Test help command itself"
        try:
            gsvn('help')
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def testOtherCommands(self):
        try:
            for cmd in get_all_cmds():
                run("python ./gsvn.py %s -h" % cmd.full_name)
            self.assertTrue(True)
        except:
            self.assertTrue(False)


if __name__ == '__main__':
    dir = os.path.dirname(__file__)
    dir and os.chdir(dir)
    unittest.main()
