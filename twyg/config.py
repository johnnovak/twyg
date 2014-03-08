import math, os, re, sys
import operator as _operator

# TODO what happens in NodeBox?
from pkg_resources import resource_filename

try:
    # Python 2.7+
    from collections import OrderedDict
except ImportError:
    # Python 2.4-2.6 & Nodebox 1
    from twyg.ordereddict import OrderedDict

from twyg.css3colors import color_to_rgba, colornames
from twyg.tree import Direction

import twyg.common


CONF_EXT = '.twg'

DEFAULTS_DIR = 'defaults'
COLORS_DIR   = 'colors'
CONFIGS_DIR  = 'configs'

DEFAULT_LEVEL = '$defaultLevel'


# This is a high-leve description of the config parsing process:
#
# 1.   Load configuration (``loadconfig``)
#
# 1.1  Read in the whole config file and tokenize it line by line using
#      regexps (``_tokenize_file``)
#
# 1.2  Build config data structure by running an FSM paraser on the
#      resulting tokens (``buildconfig``). @copy and @include directives
#      are fully resolved during the parsing process:
#
#      - @copy directives are expanded.
#
#      - If an @include directive is encountered, the referenced config file
#        is loaded and tokenized by ``_tokenize_file`` and then recursively
#        parsed by ``buildconfig``.
#
# 2.   TODO
#


class ConfigError(Exception):
    """ Exception for displaying configuration error messages in a
    normalized format.
    """
    def __init__(self, msg, token=None, file=None, line=None, col=None):
        self.msg = msg
        if token:
            self.file = token.file
            self.line = token.line
            self.col = token.col
        else:
            self.file = file
            self.line = line
            self.col = col

    def __str__(self):
        return ("Error in configuration file '%s' on line %s at column %s: "
                "\n  %s" % (self.file, self.line, self.col, self.msg))


##############################################################################
# Tokenizer
##############################################################################

class Pattern(object):
    """ Token ID and regexp pattern pair used for tokenization.
    """
    def __init__(self, id, pattern):
        self.id = id
        self.pattern = pattern

# Tokenization rules used for tokenizing a config file.
# The ordering is important.
rules = [
    Pattern('(whitespace)', r'^([ \t]+)'),
    Pattern('(comment)',    r'^(--.*)'),
    Pattern('(section)',    r'^\[([a-zA-Z]+)\]'),
    Pattern('(level)',      r'^{([a-zA-Z][a-zA-Z0-9_]*)}'),
    Pattern('(directive)',  r'^@([a-zA-Z]+)'),
    Pattern('(float)',      r'^([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)'),
    Pattern('(percent)',    r'^([0-9][0-9]*%)'),
    Pattern('(integer)',    r'^([0-9][0-9]*)'),
    Pattern('(operator)',   r'^(\+|-|\*|/|\^|\(|\)|\[|\]|\.|,)'),
    Pattern('(name)',       r'^([a-zA-Z][a-zA-Z0-9_]*)'),
    Pattern('(hexcolor)',   r'^(#[a-zA-Z0-9]+)'),
    Pattern('(string)',     r'^"([^"\\]*(?:\\.[^"\\]*)*)"')
]


def tokenize(config, file=None, flat=False):
    """ Convert a configuration into a list of tokens that can then be
    parsed further.
    """

    lines = config.split('\n');

    def linenum(line_nr, flat):
        return line_nr if flat else line_nr + 1

    tokens = []

    for line_nr, line in enumerate(lines):
        line = line.strip()
        if not line:
            sym = symbol('(newline)')
            tokens.append(sym())
            continue
        col = 1

        while line:
            found = False
            for r in rules:
                m = re.match(r.pattern, line)
                if m:
                    val = m.group(1)
                    id = r.id
                    if id != '(whitespace)' and id != '(comment)':
                        if id == '(operator)':
                            sym = symbol_table.get(val)
                            if not sym:
                                raise ConfigError(
                                    "Syntax error: unknown operator: '%s'"
                                    % val, file=file,
                                    line=linenum(line_nr, flat), col=col)
                        else:
                            sym = symbol_table[id]

                        s = sym()
                        s.value = val
                        s.file = file
                        s.line = linenum(line_nr, flat)
                        s.col = col
                        tokens.append(s)

                    end = m.end(0)
                    line = line[end:]
                    col += end
                    found = True
                    break

            if not found:
                raise ConfigError("Syntax error",
                                  file=file, line=linenum(line_nr, flat),
                                  col=col)

        sym = symbol('(newline)')
        tokens.append(sym())

    return tokens


##############################################################################
# Config level FSM parser
##############################################################################

def buildconfig(tokens, cwd=None, state='start', config=None, curr=None,
                curr_section=None, curr_level=None, section_props=False,
                prev_configs=[]):

    """ Build the final config dict from the results of the config file
    tokenization step.

    The implementation is a simple FSM parser with some internal state.
    Most of the complexity comes from the error handling and the
    building of meaningful error messages.

    @copy directives are fully expanded. If an @include directive is
    encountered, tokenize the included config file and recursively call
    buildconfig on the result.

    Below is a simple config file and the corresponding data structure
    as built by this function. Note that the tokenization step is not
    handled by this function.


    [connection]
        style                   junction
        linewidth               3
        cornerRadius            10
        cornerStyle             rounded

    [node]
      {normal}
        style                   rect
        strokeWidth             3
        cornerRadius            40

      {root}
        @copy normal
        levelDepthMax           0
        cornerRadius            80

      {leaf}
        @copy normal
        levelNumChildrenMax     0
        cornerRadius            1

    -----------------------------------------------------------------

    {
        'connection': OrderedDict([
            ('style',          [((name) junction), ((end) None)]),
            ('linewidth',      [((integer) 3), ((end) None)]),
            ('cornerRadius',   [((integer) 10), ((end) None)]),
            ('cornerStyle',    [((name) rounded), ((end) None)])
        ),

        'node': OrderedDict([
            ('normal', {
                'style':         [((name) rect), ((end) None)],
                'strokeWidth':   [((integer) 3), ((end) None)],
                'cornerRadius':  [((integer) 40), ((end) None)]
            }),
            ('root', {
                'style':         [((name) rect), ((end) None)],
                'strokeWidth':   [((integer) 3), ((end) None)],
                'levelDepthMax': [((integer) 0), ((end) None)],
                'cornerRadius':  [((integer) 80), ((end) None)]
            }),
            ('leaf', {
                'style':               [((name) rect), ((end) None)],
                'strokeWidth':         [((integer) 3), ((end) None)],
                'levelNumChildrenMax': [((integer) 0), ((end) None)],
                'cornerRadius':        [((integer) 1), ((end) None)]
            })
        ])
    }
    """

    def isliteral(id):
        return id in ('(operator)', '(float)', '(percent)', '(integer)',
                      '(name)', '(hexcolor)', '(string)')

    # TODO Python bug ???
    if not config:
        config = dict()

    for t in tokens:
        if state == 'start':
            if t.id == '(newline)':
                pass
            elif t.id == '(section)':
                state = 'section'
                curr_section = t.value
                # The order of the levels within a section must be
                # retained
                curr = config[curr_section] = OrderedDict()
                curr_level = None
                section_props = False
            else:
                raise ConfigError('Configuration must start with a '
                                  'section definition', t)

        elif state == 'section':
            if t.id == '(newline)':
                state = 'in_section'
            else:
                raise ConfigError("Section definition '%s' must be followed "
                                  'by a newline' % curr_section, t)

        elif state == 'in_section':
            if t.id == '(newline)':
                pass
            elif t.id == '(name)':
                state = 'property'
                name = t.value
                value = []
                if not curr_level:
                    section_props = True

            elif t.id == '(section)':
                section = t.value
                if section in config:
                    raise ConfigError('Duplicate section definition '
                                      "'%s'" % section, t)
                state = 'section'
                curr_section = section
                # The order of the levels within a section must be
                # retained
                curr = config[curr_section] = OrderedDict()
                curr_level = None
                section_props = False

            elif t.id == '(level)':
                level = t.value
                if section_props:
                    raise ConfigError("Invalid level definition '%s' in "
                                      "section '%s':\n"
                                      "\tlevel definitions are "
                                      "not allowed after section level "
                                      "properties"
                                      % (level, curr_section), t)

                if level in config[curr_section]:
                    raise ConfigError("Duplicate level name '%s' in "
                                      "section '%s'"
                                      % (level, curr_section), t)
                state = 'level'
                curr_level = level
                curr = config[curr_section][curr_level] = {}

            elif t.id == '(directive)':
                d = t.value
                if d not in ('include', 'copy'):
                    raise ConfigError("Invalid directive: '%s'" % d, t)
                state = 'directive'
                name = t.value
                value = []
            else:
                raise ConfigError('Property name, level definition or '
                                  'directive expected', t)

        elif state == 'level':
            if t.id == '(newline)':
                state = 'in_section'
            else:
                raise ConfigError("Level definition '%s' in section '%s' "
                                  'must be followed by a newline'
                                  % (curr_level, curr_section), t)

        elif state == 'directive':
            if t.id == '(newline)':
                if not value:
                    p = prevtoken
                    raise ConfigError("Missing parameter for directive '%s'"
                                      % name, p)
                state = 'in_section'
                param = ''.join([v.value for v in value])

                if name == 'include':
                    try:
                        configpath = include_path(os.path.join(cwd, param))

                        if configpath in prev_configs:
                            raise ConfigError(
                                "Error while processing '%s' directive:\n"
                                "\tCircular reference detected when "
                                "attempting to include '%s'"
                                % (name, configpath), prevtoken)

                        tokens, cwd = _tokenize_file(configpath, flat=False)
                    except IOError, e:
                        raise ConfigError(
                            "Error while processing '%s' directive:\n"
                            "\t%s: '%s'" % (name, e.strerror, e.filename),
                            prevtoken)

                    prev_configs.append(configpath)
                    buildconfig(tokens, cwd, state, config, curr,
                                curr_section, curr_level, section_props,
                                prev_configs)

                elif name == 'copy':
                    level = param
                    if level not in config[curr_section]:
                        t = prevtoken
                        raise ConfigError(
                                "Error while processing '%s' directive:\n"
                                "\tLevel '%s' does not exist in section '%s'"
                                % (name, level, curr_section), t)

                    curr.update(config[curr_section][level])

            elif isliteral(t.id):
                value.append(t)
            else:
                raise ConfigError('Invalid directive syntax', t)

        elif state == 'property':
            if t.id == '(newline)':
                raise ConfigError("Missing property expressions for property "
                                  "'%s'" % name, prevtoken)
            if t.isoperator('['):
                state = 'array'
                value.append(t)
            elif isliteral(t.id):
                state = 'in_property'
                value.append(t)
            else:
                raise ConfigError("Property expressions cannot start with "
                                  "'%s'" % t.value, t)

        elif state == 'in_property':
            if isliteral(t.id):
                value.append(t)
            elif t.id == '(newline)':
                state = 'in_section'
                sym = symbol('(end)')
                value.append(sym())
                curr[name] = value
            else:
                raise ConfigError("Syntax error in property expressions '%s'"
                                  % name, t)

        elif state == 'array':
            if t.id == '(newline)':
                pass
            elif t.isoperator('['):
                raise ConfigError('Arrays cannot be nested', t)
            elif t.isoperator(']'):
                state = 'end_array'
                value.append(t)
            elif isliteral(t.id):
                value.append(t)
            else:
                raise ConfigError("Syntax error in property expressions '%s'"
                                  % name, t)

        elif state == 'end_array':
            if t.id == '(newline)':
                state = 'in_section'
                sym = symbol('(end)')
                value.append(sym())
                curr[name] = value
            else:
                raise ConfigError("End of array symbol ']' must be followed"
                                  'by a newline', t)

        prevtoken = t

    return config


def _tokenize_file(file, flat=False):
    """ Tokenize a config file.

    Returns the list of tokens and the directory the config file resides
    in (this will be used for processing the @include directives).
    """
    f = open(file)
    config = f.read()
    if flat:
        config = '[default]\n' + config
    tokens = tokenize(config, file, flat=flat)
    cwd = os.path.dirname(file)
    return tokens, cwd


def loaddefaults(defaults):
    return loadconfig(defaults_path(defaults), flat=True)


def loadconfig(file, flat=False):
    """ Tokenize a config file.

    If ``flat`` is true, all properties will be placed in a section
    called 'default'. This should only be used when tokenizing config
    defaults that don't contain a section definition.

    # TODO's
    See buildconfig for a detailed description of the returned config
    data structure.
    """

    tokens, cwd = _tokenize_file(file, flat)
    config = buildconfig(tokens, cwd=cwd, prev_configs=[file])
    if flat:
        config = config['default']
    return config


def find_config(paths, name):
    """ Find a config file.

    ``paths`` contains a list of search paths, including the name of the
    config. The function first tries to fint the config as specified in
    the path, then tries with CONF_EXT extension appended at the end.
    """

    for p in paths:
        if os.path.exists(p):
            return p
        p2 = p + CONF_EXT
        if os.path.exists(p2):
            return p2
    raise ConfigError("Cannot open %s file: '%s'" % (name, p))


def defaults_path(configname):
    conf = os.path.join(DEFAULTS_DIR, configname)
    home_conf = os.path.join(twyg.common.TWYG_HOME, conf)
    paths = [
        home_conf,
        resource_filename(__name__, conf)
    ]
    return find_config(paths, 'defaults config')


def colors_path(configname):
    colors_conf = os.path.join(COLORS_DIR, configname)
    home_colors_conf = os.path.join(twyg.common.TWYG_HOME, colors_conf)
    paths = [
        configname,
        home_colors_conf,
        resource_filename(__name__, colors_conf)
    ]
    return find_config(paths, 'colorscheme config')


def config_path(configname):
    configs_conf = os.path.join(CONFIGS_DIR, configname)
    home_configs_conf = os.path.join(twyg.common.TWYG_HOME, configs_conf)
    paths = [
        configname,
        home_configs_conf,
        resource_filename(__name__, configs_conf)
    ]
    return find_config(paths, 'config')


def include_path(configname):
    return find_config([configname], 'included config')


##############################################################################
# Pratt expression parser
##############################################################################

# Top-down operator-precedence parser based heavily on Fredrik Lundh's
# excellent article on Pratt parsers:
#
# http://effbot.org/zone/simple-top-down-parsing.htm
#
# Added type checking, function calls and extensive error reporting on
# my own.
#
# Further references:
#
# http://eli.thegreenplace.net/2010/01/02/top-down-operator-precedence-parsing/
# http://javascript.crockford.com/tdop/tdop.html

def parsecolor(mode, *components):
    """ Helper function to parse colors specified by their individual
    component values using the CSS3 color parser.
    """
    s = ', '.join([str(a) for a in components])
    if mode:
        s = mode + '(' + s + ')'
    return _ctx.color(*color_to_rgba(s))


# Functions that are available in a config file
function_table = {
    'abs':      abs,
    'ceil':     math.ceil,
    'floor':    math.floor,
    'log':      math.log,
    'log10':    math.log10,
    'max':      max,
    'min':      min,
    'pow':      pow,
    'round':    round,
    'sqrt':     math.sqrt,

    'rgb':      lambda r, g, b:    parsecolor('rgb',  r, g, b),
    'rgba':     lambda r, g, b, a: parsecolor('rgba', r, g, b, a),
    'hsl':      lambda h, s, l:    parsecolor('hsl',  h, s, l),
    'hsla':     lambda h, s, l, a: parsecolor('hsla', h, s, l, a)
}


variable_table_defaults = {
}

variable_table = {
}

def init_variable_table_defaults():
    # Make all named CSS3 colors available as color.<colorname> in the
    # config file
    def inject_css3_colors():
        global variable_table_defaults

        class Colors:
            pass

        col = Colors()
        for name in colornames.keys():
            setattr(col, name, parsecolor(None, name))
        variable_table_defaults['color'] = col

    inject_css3_colors()


class SymbolBase(object):
    id = None
    value = None
    first = second = None

    def nud(self):
        raise ConfigError("Syntax error: '%s'" % self.value, self)

    def led(self, *args):
        raise ConfigError("Syntax error: unknown operator: '%s'"
                          % self.value, self)

    def __repr__(self):
        if self.id == '(operator)':
            out = ["'" + self.value + "'", self.first, self.second]
            out = map(str, filter(None, out))
            return "(" + " ".join(out) + ")"
        else:
            return '(%s %s)' % (self.id, self.value)

    def isoperator(self, op):
        return self.id == '(operator)' and self.value == op


symbol_table = {}

def symbol(id, value=None, bp=0):
    key = value if value else id
    if key in symbol_table:
        s = symbol_table[key]
    else:
        class s(SymbolBase): pass

        s.__name__ = 'symbol-' + key
        s.id = id
        s.lbp = bp
        s.value = value
        symbol_table[key] = s

    s.lbp = max(bp, s.lbp)
    return s

def operator(op, bp=None):
    return symbol('(operator)', op, bp)

def infix(op, bp):
    def led(self, left):
        self.first = left
        self.second = expression(bp)
        return self
    operator(op, bp).led = led

def prefix(op, bp):
    def nud(self):
        self.first = expression(bp)
        self.second = None
        return self
    operator(op).nud = nud

def method(s):
    assert issubclass(s, SymbolBase)
    def bind(fn):
        setattr(s, fn.__name__, fn)
    return bind


# Grammar description
infix('+', 10); infix('-', 10)
infix('*', 20); infix('/', 20); infix('%', 20)
prefix('+', 30); prefix('-', 30)
operator('.', 40); operator('[', 40); operator('(', 40)


@method(symbol('('))
def nud(self):
    expr = expression()
    advance(')')
    return expr

operator(')'); operator(',')

@method(symbol('('))
def led(self, left):
    self.first = left
    self.second = []
    if not token.isoperator(')'):
        while 1:
            self.second.append(expression())
            if not token.isoperator(','):
                break
            advance(',')
        advance(')')
    return self

@method(symbol('.'))
def led(self, left):
    self.first = left
    self.second = token
    advance()
    return self


operator(']')

@method(symbol('['))
def nud(self):
    self.first = []
    if not token.isoperator(']'):
        while 1:
            if token.isoperator(']'):
                break
            self.first.append(expression())
            if not token.isoperator(','):
                break
            advance(',')
        advance(']')
        return self


symbol('(section)')
symbol('(level)')
symbol('(directive)')
symbol('(newline)')
symbol('(end)')


nud = lambda self: self

symbol('(float)').nud = nud
symbol('(percent)').nud = nud
symbol('(integer)').nud = nud
symbol('(name)').nud = nud
symbol('(hexcolor)').nud = nud
symbol('(string)').nud = nud


# Evaluation rules
opnames = {
    'add': '+',
    'pos': '+',
    'sub': '-',
    'neg': '-',
    'mul': '*',
    'div': '/'
}

def unaryop(t, op):
    try:
        a = t.first.eval()
        return op(a)
    except TypeError, e:
        raise ConfigError("Cannot use operator '%s' on type '%s'"
                          % (opnames[op.__name__], type(a).__name__), t)

def binaryop(t, op):
    try:
        a = t.first.eval()
        b = t.second.eval()
        # Ensure that an int/int division always results in a float
        # result
        if type(b) == int:
            b = float(b)
        return op(a, b)
    except TypeError, e:
        raise ConfigError("Cannot use operator '%s' on types '%s' and '%s'"
                          % (opnames[op.__name__], type(a).__name__,
                             type(b).__name__), t)

@method(symbol('+'))
def eval(self):
    if self.second:
        return binaryop(self, _operator.add)
    else:
        return unaryop(self, _operator.pos)

@method(symbol('-'))
def eval(self):
    if self.second:
        return binaryop(self, _operator.sub)
    else:
        return unaryop(self, _operator.neg)

symbol('*').eval = lambda self: binaryop(self, _operator.mul)
symbol('/').eval = lambda self: binaryop(self, _operator.div)


def isfunction(o):
    return type(o).__name__ in ('function', 'instancemethod',
                                'builtin_function_or_method')

@method(symbol('('))
def eval(self):
    if self.first.isoperator('.'):
        dot_op = self.first
        obj, attr = dot_operator(dot_op)
        if not hasattr(obj, attr):
            raise ConfigError("'%s' has no method named '%s'" %
                              (dot_op.first.value, attr), dot_op.second)
        fn = getattr(obj, attr)
    else:
        fn = self.first.value
        if fn not in function_table:
            raise ConfigError("Function '%s' does not exist" % fn, self.first)
        fn = function_table[fn]
    args = self.second
    a = [x.eval() for x in args]
    try:
        return fn(*a)
    except TypeError, e:
        raise ConfigError(str(e).capitalize(), self)


@method(symbol('.'))
def eval(self):
    obj, attr = dot_operator(self)
    if not hasattr(obj, attr):
        raise ConfigError("'%s' has no property named '%s'"
                          % (self.first.value, attr), self.second)
    a = getattr(obj, attr)
    if isfunction(a):
        raise ConfigError("'%s' is a method of '%s'; it cannot be used as "
                          'a property ' % (attr, self.first.value),
                          self.second)
    return a


def dot_operator(t):
    i = t.first.id
    v = t.first.value
    if i == '(name)':
        if v not in variable_table:
            raise ConfigError("Variable '%s' does not exist" % v, t)
        obj = variable_table[v]
    else:
        obj = t.first.eval()
    attr = t.second.value
    return obj, attr


@method(symbol('['))
def eval(self):
    args = self.first
    a = [x.eval() for x in args]
    return a


symbol('(float)').eval    = lambda self: float(self.value)
symbol('(integer)').eval  = lambda self: int(self.value)
symbol('(percent)').eval  = lambda self: self.value
symbol('(hexcolor)').eval = lambda self: parsecolor(None, self.value)
symbol('(string)').eval   = lambda self: self.value.replace('\\"', '"')


@method(symbol('(name)'))
def eval(self):
    v = self.value
    if v not in variable_table:
        raise ConfigError("Variable '%s' does not exist" % v, self)
    return variable_table[v]


# Pratt parser
def nexttoken():
    global token, lasttoken
    t = token
    if t.id != '(end)':
        lasttoken = t
    token = next()
    return t

def expression(rbp=0):
    global token, lasttoken
    t = nexttoken()
    left = t.nud()
    while rbp < token.lbp:
        t = nexttoken()
        left = t.led(left)
    return left

def advance(value=None, id='(operator)'):
    global token
    if value and not (token.id == id and token.value == value):
        raise ConfigError("Syntax error: expected '%s'" % value, lasttoken)
    token = next()


def parse_expr(expr):
    global next, token

    next = (x for x in expr).next
    token = next()
    try:
        e = expression()
    except StopIteration:
        raise ConfigError("Premature end of expression", lasttoken)

    if token.id != '(end)':
        raise ConfigError("Expression should have ended at this point", token)

    return e


def eval_expr(expr, vars={}):
    global variable_table
    if not variable_table_defaults:
        init_variable_table_defaults()
    variable_table = dict(variable_table_defaults)
    variable_table.update(vars)
    return expr.eval()


##############################################################################
# Levels
##############################################################################

class Level(object):
    """ Class for holding and evaluating level selector rules. """

    def __init__(self, levelname, config={}):
        self.levelname = levelname

        # The ordinal numbers of the first four enum values must be
        # identical to those of the Direction enum.
        Level.orientation = ('top', 'right', 'bottom', 'left', 'any')

        properties = {
            'levelDepthMin':       (NumberProperty, {'min': 0}),
            'levelDepthMax':       (NumberProperty, {'min': 0}),
            'levelNumChildrenMin': (NumberProperty, {'min': 0}),
            'levelNumChildrenMax': (NumberProperty, {'min': 0}),
            'levelOrientation':    (EnumProperty,
                                    {'values': Level.orientation})
        }

        self._props = Properties(properties, 'level.twg', config,
                                 extra_prop_warning=False)
        self._eval()

    def __repr__(self):
        return self.levelname

    def _eval(self):
        E = self._props.eval

        self.depth_min       = E('levelDepthMin')
        self.depth_max       = E('levelDepthMax')
        self.numchildren_min = E('levelNumChildrenMin')
        self.numchildren_max = E('levelNumChildrenMax')

        o = E('levelOrientation')
        if o == 'any':
            self.orientation = -1
        else:
            self.orientation = Level.orientation.index(o)

    def selects(self, node, layout):
        """ Check if the this level's selector rules select a given
        node.

        The layout object must be passed to determine the orientation of
        the node in certain layouts.
        """

        depth = node.depth()
        numchildren = len(node.getchildren())
        o = layout.node_orientation(node)

        ok = (    depth >= self.depth_min
              and depth <= self.depth_max
              and numchildren >= self.numchildren_min
              and numchildren <= self.numchildren_max)

        # -1 stands for 'any' orientation, which means the orientation
        # can be any valid value, so we don't need to do the orientation
        # filtering
        if self.orientation >= 0:
            ok = ok and self.orientation

        return ok


def createlevel(levelname, config):
    """ Create Level object from a config and then deletes all level
    related properties.
    """
    level = Level(levelname, config)
    for k in level._props._properties.keys():
        if k in config:
            del config[k]
    return level


class SectionLevel(object):
    """ Placeholder to keep level descriptions and drawer objects
    together. """

    def __init__(self, level, drawer):
        self.level = level
        self.drawer = drawer

    def __repr__(self):
        return '{%s}: %s' % (self.level, self.drawer)


STYLE             = 'style'
LAYOUT_CONFIG     = 'layout'
NODE_CONFIG       = 'node'
CONNECTION_CONFIG = 'connection'
COLOR_CONFIG      = 'color'


##############################################################################
# Properties
##############################################################################

class Property(object):
    def __init__(self, name):
        self.name = name

    def eval(self, vars):
        self.value = eval_expr(self.expr, vars)
        self._validate()
        return self.value


class StringProperty(Property):
    def _validate(self):
        if type(self.value) not in (str, unicode):
            raise ConfigError("Property '%s' must evaluate to a string"
                              % self.name, self.expr[0])


class NumberProperty(Property):
    def __init__(self, name, min=None, max=None):
        super(NumberProperty, self).__init__(name)
        self.min = min
        self.max = max

    def _validate(self):
        if type(self.value) not in (int, float):
            raise ConfigError("Property '%s' must evaluate to a number"
                              % self.name, self.expr)

        if self.min and self.value < self.min:
            raise ConfigError(
                "Number property '%s' must have a value greater "
                "than %s" % (self.name, self.min), self.expr)

        if self.max and self.value > self.max:
            raise ConfigError("Number property '%s' must have a value less "
                              "than %s" % (self.name, self.max), self.expr)


class ColorProperty(Property):
    def _validate(self):
        if type(self.value).__name__ != 'Color':
            raise ConfigError("Property '%s' must evaluate to a color"
                              % self.name, self.expr)


class EnumProperty(Property):
    def __init__(self, name, values):
        super(EnumProperty, self).__init__(name)
        self.values = values

    def eval(self, vars):
        enumvars = {}
        for value, name in enumerate(self.values):
            enumvars[name] = value
        vars.update(enumvars)
        n = eval_expr(self.expr, vars)

        if type(n) not in (int, float):
            raise ConfigError(
                ("Enum property '%s' must evaluate to a numeric value"
                 % self.name), self.expr)

        n = int(round(n))
        if n < 0 or n >= len(self.values):
            raise ConfigError(
                ("Enum property '%s' evaluated to an invalid "
                 "numeric value: %s" % (self.name, n)), self.expr)

        self.value = self.values[n]
        return self.value


class BooleanProperty(Property):
    def eval(self, vars):
        vars = {'no': 0, 'off': 0, 'false': 0, 'yes': 1, 'on': 1, 'true': 1}
        n = eval_expr(self.expr, vars)

        if type(n) not in (int, float):
            raise ConfigError(
                ("Boolean property '%s' must evaluate to a numeric value"
                 % self.name), self.expr)

        self.value = True if n > 0.0 else False
        return self.value


class ArrayProperty(Property):
    def __init__(self, name, type):
        super(ArrayProperty, self).__init__(name)
        self.type = type

    def _validate(self):
        # TODO array element type validation
        if type(self.value) != list:
            raise ValueError


class Properties(object):
    """ Class for managing configuration properties. """

    def __init__(self, properties, defaults, config, extra_prop_warning=True):
        """
        Load and parse the default config file ``default`` and merge it
        with the configuration ``config`` (defaults will be
        overwritten).

        The ``properties`` dict contains the list of allowed properties
        where the key is the name of the property and the value a
        two-element tuple of which the first element is the class of the
        property and the second element the property's extra parameters
        (note that some property types have mandatory extra parameters,
        e.g. ArrayProperty). For example:

        {
            'fontName':  (StringProperty, {}),
            'fontSizes': (ArrayProperty,  {'type': NumberProperty})
        }

        Warn on property names that are not listed in the ``properties``
        dict if ``extra_prop_warning`` is True.
        """

        c = loaddefaults(defaults)
        c.update(config)
        config = c

        # Build properties dictionary
        self._properties = {}
        for name, prop_params in properties.iteritems():
            # The first parameter is the property class, the second the
            # optional constructor parameters
            prop_class, opts = prop_params
            self._properties[name] = prop_class(name, **opts)

        for name, prop in self._properties.iteritems():
            if name not in config:
                raise ConfigError("Missing property: '%s'" % name)
            e = parse_expr(config[name])
#            print '>>>', name, ':', e
            prop.expr = e
            prop.name = name

        if extra_prop_warning:
            self._warn_extra_props(config)

    def _warn_extra_props(self, config):
        extra_props = set(config.keys()) - set(self._properties.keys())
        for p in extra_props:
            token = config[p][0]
            #TODO make displaying warnings optional? print to stdout?
            print >>sys.stderr, (
                "Warning: Unknown property '%s' in configuration "
                "file '%s' on line %s" % (p, token.file, token.line))

    def eval(self, name, scope=None, vars={}):
        """ Evaluate the value of a property.

        ``name`` is the name of the property, ``scope`` the object in
        whose context the property is to be evaluated and ``vars``
        contains a dict of variable name and value pairs that will be
        injected into the evaluation scope.
        """

        if name not in self._properties:
            # TODO more detailed error message
            raise AttributeError("Property '%s' does not exist" % name)

        p = self._properties[name]
        if scope:
            for propname, varname in scope.property_mappings.iteritems():
                if hasattr(scope, propname):
                    vars[varname] = getattr(scope, propname)
                # TODO triggered by 'basecolor' -- why?
#                else:
#                    raise ConfigError("Variable '%s' is not evaluated "
#                                      "at this point" % (varname))

        return p.eval(vars)


##############################################################################
# Utils
##############################################################################

def format_paramvalue_error(configname, paramname, value, correct_type):
    msg = ("Invalid %s parameter value: %s: %s ('%s', should be '%s')"
           % (configname, paramname, value, correct_type))
    return msg


def get_stylename(configname, config):
    if STYLE not in config:
        raise ConfigError, ("Style must be specified in '%s'" % (configname))

    expr = config[STYLE]
    if len(expr) == 2 and expr[0].id == '(name)' and expr[1].id == '(end)':
        stylename = expr[0].value
    else:
        raise ConfigError("Invalid style name", expr[0])

    if not (type(stylename) == str or type(stylename) == unicode):
        raise ConfigError, format_paramvalue_error(configname, STYLE,
                                                   stylename, str)
    return stylename

