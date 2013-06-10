try:
    # Included in Python 2.6 by default
    import json

except ImportError:
    # simplejson is required for Python 2.5
    import simplejson as json


import twyg.colorizer
import twyg.connection
import twyg.node

from twyg.config import (NODE_CONFIG, CONNECTION_CONFIG, LAYOUT_CONFIG,
                         COLOR_CONFIG, STYLE, Level, SectionLevel, ConfigError,
                         get_stylename, loadconfig, createlevel)
from twyg.layout import layout_by_name
from twyg.tree import Tree


# TODO remove
reload(twyg.colorizer)
reload(twyg.connection)
reload(twyg.node)


_initialized = False


def _fullname(o):
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__
    return module + '.' + o.__class__.__name__


def _detect_nodebox():
    try:
        return _fullname(_ctx) == 'nodebox.graphics.Context'
    except NameError:
        return False


def _init():
    global _initialized
    if _initialized:
        return

    nodebox = _detect_nodebox()
    if nodebox:
        global _ctx
    else:
        from twyg.cairowrapper import context as _ctx

    twyg.common.init(nodebox=nodebox, ctx=_ctx)

    # Pass drawing context to the modules that need access to drawing
    # functions (we need to it this way to keep compatibility with
    # NodeBox)
    twyg.colorizer._ctx = _ctx
    twyg.common._ctx = _ctx
    twyg.connection._ctx = _ctx
    twyg.node._ctx = _ctx
    twyg.tree._ctx = _ctx

    _initialized = True


def _loadjson(fname):
    fp = file(fname)
    data = json.load(fp)
    fp.close()
    return data


def _has_levels(d):
    # TODO bit of a hack...
    num_dicts = [x for x in d.values() if type(x) == dict]
    return len(num_dicts) == len(d)


def _get_style(section, config):
    style = get_stylename(section, config)
    del config[STYLE]
    return style


def _create_drawers(config, section, factory_func, constr_args=()):
    """ Create a list of SectionLevel objects for a given configuration
    section from a full configuration. """

    c = config[section]
    level_dict = c if _has_levels(c) else {'defaultLevel': c}
    drawers = []

    for level_name, conf in level_dict.iteritems():
        style = _get_style(section + '.' + level_name, conf)
        level = createlevel(conf)
        drawer_class = factory_func(style)
        drawer = drawer_class(conf, *constr_args)
        drawers.append(SectionLevel(level, drawer))

    return drawers


def buildtree(data_fname, config_fname, colorscheme_fname):
    _init()

    data = _loadjson(data_fname)
    config = loadconfig(config_fname)
    colorscheme = loadconfig(colorscheme_fname, flat=True)

    # Layout section
    section = LAYOUT_CONFIG
    c = config[section]
    if _has_levels(c):
        # TODO more detail
        raise Exception('Layout section cannot have levels')
    style = _get_style(section, c)
    layout_cls = layout_by_name(style)
    layout = layout_cls(c)

    nodedrawers = _create_drawers(config, NODE_CONFIG,
                                  factory_func=twyg.node.nodedrawer_by_name)

    conndrawers = _create_drawers(config, CONNECTION_CONFIG,
                                  factory_func=twyg.connection.conndrawer_by_name)

    colorizers = _create_drawers(config, COLOR_CONFIG,
                                 factory_func=twyg.colorizer.colorizer_by_name,
                                 constr_args=(colorscheme,))

    return Tree(layout, nodedrawers, conndrawers, colorizers, data)

