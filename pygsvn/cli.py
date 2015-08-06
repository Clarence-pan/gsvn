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

def run_check_confirm(cmd, *args, **kwargs):
    _print_prompt(cmd)
    try:
        return subprocess.check_call(cmd, *args, **kwargs)
    except subprocess.CalledProcessError as e:
        print "Warnning: ", e
        if confirm("Would you like to continue?", 'Yn') == 'n':
            raise
        else:
            return e.returncode

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


def confirm(prompt, options):
    default_option = None
    for x in options:
        if x.isupper():
            default_option = x
            break

    prompt = "%s [%s]" % (prompt, options)
    options = [x.lower() for x in options]

    while True:
        input = raw_input(prompt)
        if default_option != None and input == "\n":
            return default_option.lower()

        if input.lower() in options:
            return input.lower()
