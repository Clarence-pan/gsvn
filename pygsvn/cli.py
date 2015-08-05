# -*- coding: utf-8 -*-
import subprocess, sys

# IS_VERBOSE_MODE = '-v' in sys.argv or '--verbose' in sys.argv
IS_VERBOSE_MODE = True

def is_verbose_mode():
    return IS_VERBOSE_MODE

def run(cmd):
    _print_prompt(cmd)
    return subprocess.call(cmd)

def run_check_return(cmd, *args, **kwargs):
    _print_prompt(cmd)
    return subprocess.check_call(cmd, *args, **kwargs)

def run_check_output(cmd):
    _print_prompt(cmd)

    if is_verbose_mode():
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            print output
            return output
        except subprocess.CalledProcessError as e:
            print e.output
            print "=> %d" % e.returncode
            raise
    else:
        return subprocess.check_output(cmd)

def _print_prompt(cmd):
    if is_verbose_mode():
        print '#', cmd

