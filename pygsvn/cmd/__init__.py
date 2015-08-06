# -*- coding: utf-8 -*-
import glob, os, inspect, pygsvn.cli
class Executor(object):
    '''
    implements how to parse arguments and how to execute commands
    '''
    def __init__(self, cmd):
        if not hasattr(cmd, 'execute'):
            raise TypeError("%s is not executable!" % cmd)

        self.cmd = cmd
        self.cmd_name = cmd.__name__.split('.').pop()

        # options: boolean values
        if hasattr(cmd, 'options'):
            cmd_options = [x for x in cmd.options] # convert to list
        else:
            cmd_options = []

        # add common options:
        cmd_options.append(Option('help', ('h', '?')))
        cmd_options.append(Option('verbose', ('v', )))

        # build options map
        self.cmd_options = dict(zip([x.name for x in cmd_options], cmd_options))

        # add options
        argspec = inspect.getargspec(cmd.execute)
        required_args_len = (argspec.args and len(argspec.args) or 0) - (argspec.defaults and len(argspec.defaults) or 0)
        if argspec.defaults:
            for k, v in zip(argspec.args[required_args_len:],argspec.defaults):
                if k not in self.cmd_options:
                    self.cmd_options[k] = Option(k, type=type(v), value=v)

        elif argspec.args:
            for k in argspec.args[:required_args_len]:
                if k not in self.cmd_options:
                    self.cmd_options[k] = Option(k, type=None, required=True)

    def execute(self, *args):
        options, rest_args = self.parse_args(args)

        # process help command
        if 'help' in options and options['help']:
            return get_cmd('help').execute(self.cmd_name)

        if 'verbose' in options and options['verbose']:
            pygsvn.cli.IS_VERBOSE_MODE = True

        argspec = inspect.getargspec(self.cmd.execute)
        if argspec.varargs is None and (len(options) + len(rest_args) > len(argspec.args)):
            raise ExecutionFailError("Too many arguments for command \"%s\"" % self.cmd_name)

        return self.cmd.execute(*rest_args, **options)

    def get_doc(self):
        doc = [self.cmd.execute.__doc__ or self.cmd_name]
        doc.append("Options:")
        doc.append("    %-10s  aliases" % 'name')
        doc.append("    -----------------------")
        for opt in self.cmd_options:
            doc.append("    %-10s%s %s" % (opt.name, (opt.required and '*' or ' '), ' '.join(opt.aliases)))
        return "\n".join(doc)

    def get_desc(self):
        doc = self.cmd.execute.__doc__ or self.cmd_name
        lines = doc.split("\n")
        for line in lines:
            line = line.strip()
            if line != '':
                return line

    def parse_args(self, args):
        '''
        parse commandline arguments.
        * '--' means all following is arguments, not options
        * '-xyz' means single char options
        * '--foo' means option 'foo'
        '''
        if len(args) == 0:
            return ({}, [])

        options = {}
        rest_args = []
        options_ended = False
        need_param = False
        for arg in args:
            if options_ended:
                if need_param:
                    need_param.set_value(arg)
                    need_param = False
                else:
                    rest_args.append(arg)
                continue

            if arg == '--':
                options_ended = True
                continue

            if arg[0] == '-':
                if len(arg) > 1 and arg[1] == '-':
                    option = self.get_option(arg[2:])
                    need_param = option.set_value()
                else:
                    for char in arg[1:]:
                        try:
                            option = self.get_option(char)
                            need_param = option.set_value()
                        except InvalidOptionError as e:
                            raise InvalidOptionError(e.message + ' Parsing "%s" failed.' % arg)
            elif need_param:
                need_param.set_value(arg)
                need_param = False
            else:
                rest_args.append(arg)

        for name, opt in self.cmd_options:
            if opt.value is not None:
                options[name] = opt.value

        return (options, rest_args)

    def get_option(self, alias=''):
        alias = alias.lower()
        if alias in self.cmd_options:
            return self.cmd_options[alias]

        for opt in self.cmd_options:
            if alias in opt.aliases:
                return opt

        raise InvalidOptionError('Unknown option "%s"!' % alias)

class Option(object):
    '''represent an option'''
    def __init__(self, name, aliases=(), type=bool, required=False, value=None):
        self.name = name
        self.aliases = aliases
        self.type = type
        self.required = required
        self.value = value
        self.default_value = value

    def set_value(self, value=None):
        """
        set value of option
        :param value: default None
        :return: need param or not
        """
        if self.type is bool:
            self.value = True
            return False
        elif value is None:
            return self
        else:
            self.value = value
            return False

class ExecutionFailError(StandardError):
    '''
    Indicate the execution has failed.
    '''
    pass

class InvalidOptionError(ExecutionFailError):
    '''
    Indicate some option is invalid.
    '''
    pass

def get_all_cmds():
    cmd_dir, _ = os.path.split(__file__)
    for filepath in glob.glob(os.path.join(cmd_dir, '*.py')):
        _, filename = os.path.split(filepath)
        basename, extname = os.path.splitext(filename)
        if basename != '__init__':
            yield (basename, get_cmd_desc(basename))

def get_cmd(cmd):
    try:
        cmd = get_cmd_from_alias(cmd)
        parent_mod = __import__('pygsvn.cmd.'+cmd)
        cmd_mod = getattr(parent_mod, 'cmd')
        return Executor(getattr(cmd_mod, cmd))
    except ImportError:
        return None

def get_cmd_doc(cmd):
    return get_cmd(cmd).get_doc() or cmd

def get_cmd_desc(cmd):
    return get_cmd(cmd).get_desc()

def get_cmd_from_alias(alias):
    alias = alias.replace('/','').replace('-','')
    all_alias = get_all_alias()
    for full_cmd, aliases in all_alias.items():
        if alias in aliases:
            return full_cmd
    return alias

def get_all_alias():
    return {
        'help': ('?', 'h', 'help'),
        'qcommit': ("qc", 'qco'),
        'commit': ('c', 'co'),
        'tsvn': ('ts',),
        'tgit': ('tg',),
        'validate': ('v', 'va'),
        'revertdebug': ('undebug', 'udbg', 'ud'),
        'applydebug': ('redebug', 'ad'),
        'status': ('st',)
    }
