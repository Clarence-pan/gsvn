# -*- coding: utf-8 -*-
import glob, os, inspect, pygsvn.cli


class Option(object):
    '''represent an option'''
    default_desc = {
        'path': 'path of working directory',
        'url': 'url of repository',
        'msg': 'message for logging'
    }

    def __init__(self, name, aliases=(), type=bool, required=False, value=None, desc=''):
        self.name = name
        self.aliases = aliases
        self.type = type
        self.required = required
        self.value = value
        self.default_value = value
        self.desc = desc and desc or (name in self.default_desc and self.default_desc[name]) or ''

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

class Executor(object):
    '''
    implements how to parse arguments and how to execute commands
    '''

    common_options = (
         Option('help', ('h', '?'), desc='show help info of this command'),
         Option('verbose', ('v', ), desc='show verbose information'),
    )

    def __init__(self, cmd):
        if not hasattr(cmd, 'execute'):
            raise TypeError("%s is not executable!" % cmd)

        self.cmd = cmd
        self.name = cmd.__name__.split('.').pop()
        self.full_name = hasattr(cmd, 'name') and cmd.name or self.name
        self.aliases = hasattr(cmd, 'aliases') and cmd.aliases or []
        self.cmd_options = None

    def get_cmd_options(self):
        if self.cmd_options is not None:
            return self.cmd_options

        # options: boolean values
        if hasattr(self.cmd, 'options'):
            cmd_options = [x for x in self.cmd.options] # convert to list
        else:
            cmd_options = []

        # add common options:
        for opt in self.common_options:
            cmd_options.append(opt)

        # build options map
        self.cmd_options = dict(zip([x.name for x in cmd_options], cmd_options))

        # add options
        argspec = inspect.getargspec(self.cmd.execute)
        required_args_len = (argspec.args and len(argspec.args) or 0) - (argspec.defaults and len(argspec.defaults) or 0)
        self.required_options = argspec.args and argspec.args[:required_args_len] or []
        self.optional_options = argspec.args and argspec.defaults and zip(argspec.args[required_args_len:],argspec.defaults) or []

        for k, v in self.optional_options:
            if k not in self.cmd_options:
                self.cmd_options[k] = Option(k, type=type(v), value=v)

        for k in self.required_options:
            if k not in self.cmd_options:
                self.cmd_options[k] = Option(k, type=None, required=True)

        # sort options
        sorted_options = {}
        for name in argspec.args:
            sorted_options[name] = self.cmd_options[name]

        for name, opt in self.cmd_options.items():
            if name not in sorted_options:
                sorted_options[name] = opt

        self.cmd_options = sorted_options
        return self.cmd_options

    def execute(self, *args):
        options, rest_args = self.parse_args(args)
        # process help command
        if 'help' in options and options['help']:
            return get_cmd('help').cmd.execute(self.full_name)

        if 'verbose' in options and options['verbose']:
            pygsvn.cli.IS_VERBOSE_MODE = True

        # remove common options if not nessary
        for opt in self.common_options:
            if opt.name in options and opt.name not in self.required_options and opt.name not in self.optional_options:
                del options[opt.name]

        argspec = inspect.getargspec(self.cmd.execute)
        if argspec.varargs is None and (len(options) + len(rest_args) > len(argspec.args)):
            raise ExecutionFailError("Too many arguments for command \"%s\"" % self.full_name)

        required_options_len = reduce(lambda sum, x: sum + ((x.required and x.value is not None) and 1 or 0), self.get_cmd_options().values(), 0)
        if required_options_len + len(rest_args) < len(self.required_options):
            raise ExecutionFailError("No enough arguments!")

        return self.cmd.execute(*rest_args, **options)

    def get_doc(self):
        doc = [self.cmd.execute.__doc__ or self.full_name]
        doc.append("Options:")
        doc.append("    %-15s %-20s desc" % ('name', 'aliases'))
        doc.append("    ---------------------------------------------------")
        for opt in self.get_cmd_options().values():
            doc.append("    %-15s %-20s %s" % ((opt.required and '*' or '') + opt.name, ' '.join(opt.aliases), opt.desc))
        return "\n".join(doc)

    def get_desc(self):
        doc = self.cmd.execute.__doc__ or self.full_name
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

        for name, opt in self.get_cmd_options().items():
            if opt.value is not None:
                options[name] = opt.value

        return (options, rest_args)

    def get_option(self, alias=''):
        alias = alias.lower()
        if alias in self.get_cmd_options():
            return self.cmd_options[alias]

        for opt in self.cmd_options.values():
            if alias in opt.aliases:
                return opt

        raise InvalidOptionError('Unknown option "%s"!' % alias)

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
            yield get_cmd(basename, from_alias=False)

def get_cmd(cmd, from_alias=True):
    try:
        if from_alias:
            cmd = get_cmd_from_alias(cmd)

        parent_mod = __import__('pygsvn.cmd.'+cmd)
        cmd_mod = getattr(parent_mod, 'cmd')
        return Executor(getattr(cmd_mod, cmd))
    except ImportError:
        return None

def get_cmd_doc(cmd):
    return get_cmd(cmd).get_doc() or cmd

def get_cmd_from_alias(alias):
    alias = alias.replace('/','').replace('-','')
    for cmd in get_all_cmds():
        if alias == cmd.name or alias in cmd.aliases:
            return cmd.name
    return alias

