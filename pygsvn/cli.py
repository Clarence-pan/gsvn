# -*- coding: utf-8 -*-
import subprocess, sys

# IS_VERBOSE_MODE = '-v' in sys.argv or '--verbose' in sys.argv
IS_VERBOSE_MODE = True

def is_verbose_mode():
    return IS_VERBOSE_MODE

def run(cmd):
    _print_prompt(cmd)
    return subprocess.call(cmd)

def run_check_output(cmd):
    _print_prompt(cmd)
    output = subprocess.check_output(cmd)

    if is_verbose_mode():
        print output

    return output

def _print_prompt(cmd):
    if is_verbose_mode():
        print '>', cmd

