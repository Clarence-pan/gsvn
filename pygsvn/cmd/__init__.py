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

    def get_long_name(self):
        import re
        if re.match('^[a-z]+$', self.name):
            return self.name

        for alias in self.aliases:
            if len(alias) != 1:
                return alias

        return self.name

    def quote(self, name=None, with_default_value=False):
        name = name or self.get_long_name()
        if self.type is bool:
            if len(name) == 1:
                return '-' + name
            else:
                return '--' + name
        elif len(name) == 1:
            return '-%s:' % name
        elif self.required:
            return '<' + name + '>'
        elif with_default_value:
            return '[%s=%s]' % (name, self.default_value)
        else:
            return '[' + name + ']'

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

        return self.cmd_options

    def get_cmd_form(self):
        form = [self.full_name]
        options = self.get_cmd_options()

        for name in self.required_options:
            opt = self.cmd_options[name]
            if opt.type is not bool:
                form.append(opt.quote())

        for name, _ in self.optional_options:
            opt = self.cmd_options[name]
            if opt.type is not bool:
                form.append(opt.quote(with_default_value=True))

        #common_option_names = [opt.name for opt in self.common_options]
        #for opt in self.cmd_options.values():
        #    if opt.type is bool and opt.name not in common_option_names:
        #        form.append(opt.quote())

        #for opt in self.common_options:
        #    form.append(opt.quote())

        return ' '.join(form)

    def execute(self, *args):
        options, rest_args = self.parse_args(args)
        # process help command
        if options.get('help', False):
            return get_cmd('help').cmd.execute(self.full_name)

        if options.get('verbose', False):
            pygsvn.cli.IS_VERBOSE_MODE = True

        # remove common options if not nessary
        for opt in self.common_options:
            if opt.name in options and opt.name not in self.required_options and opt.name not in self.optional_options:
                del options[opt.name]

        argspec = inspect.getargspec(self.cmd.execute)
        if argspec.varargs is None and (len(options) + len(rest_args) > len(argspec.args)):
            raise ExecutionFailError("Too many arguments for command \"%s\"" % self.full_name)

        required_rest_len = reduce(lambda sum, x: \
                                        sum - ((x.required and x.name in options) and 1 or 0), \
                                   self.get_cmd_options().values(),\
                                   len(self.required_options))
        if required_rest_len > len(rest_args):
            raise ExecutionFailError("No enough arguments!")

        return self.cmd.execute(*rest_args, **options)

    def get_doc(self):
        doc = [self.cmd.execute.__doc__ or self.full_name]
        doc.append('')
        doc.append("Options:")
        doc.append("    %-15s %-20s desc" % ('name', 'aliases'))
        doc.append("    ---------------------------------------------------")
        options = self.get_cmd_options()
        names = self.required_options + \
                [ k for k, v in self.optional_options] + \
                [ opt.name for opt in self.common_options]
        for name in names:
            opt = options[name]
            doc.append("    %-15s %-20s %s" % (opt.quote(), ' '.join([opt.quote(x) for x in opt.aliases if x != opt.get_long_name()]), opt.desc))
        return "\n".join(doc)

    def get_desc(self):
        doc = self.cmd.execute.__doc__ or self.full_name
        lines = doc.split("\n")
        for line in lines:
            line = line.strip()
            if line != '':
                return line

    def parse_args(self, args):
        import getopt
        shortopts = []
        longopts = []

        for opt in self.get_cmd_options().values():
            longopts.append(opt.name)
            for alias in opt.aliases:
                if len(alias) == 1:
                    shortopts.append(alias + (opt.type is not bool and ':' or ''))
                else:
                    longopts.append(alias + (opt.type is not bool and '=' or ''))

        options, rest_args = getopt.getopt(args, ''.join(shortopts), longopts)

        options_map = {}
        for k, v in options:
            opt = self.get_option(k.lstrip('-'))
            options_map[opt.name] = opt.type is bool and True or v

        return (options_map, rest_args)

    def parse_args_old(self, args):
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
        options = self.get_cmd_options()
        if alias in options:
            return options[alias]

        for opt in options.values():
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
    cmd_dir = os.path.dirname(__file__)
    for filepath in glob.glob(os.path.join(cmd_dir, '*.py')):
        filename = os.path.basename(filepath)
        basename, extname = os.path.splitext(filename)
        if basename != '__init__':
            yield get_cmd(basename, from_alias=False)

def get_cmd(cmd, from_alias=True):
    try:
        if from_alias:
            return get_cmd_from_alias(cmd)

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
            return cmd
    return None

