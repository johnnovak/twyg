try:
    # Python 2.6+
    import json
except ImportError:
    # Python 2.5 & Nodebox 1
    import simplejson as json


import twyg.colorizer
import twyg.connection
import twyg.node

from twyg.config import (NODE_CONFIG, CONNECTION_CONFIG, LAYOUT_CONFIG,
                         COLOR_CONFIG, STYLE, Level, SectionLevel, ConfigError,
                         get_stylename, loadconfig, createlevel)

from twyg.layout import layout_by_name
from twyg.tree import Tree


# TODO remove - for NodeBox testing only
reload(twyg.colorizer)
reload(twyg.connection)
reload(twyg.node)


_initialized = False


def _fullname(o):
    """ Get the fully qualified class name of an object. """
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__
    return module + '.' + o.__class__.__name__


def _detect_nodebox():
    """ Return True if NodeBox 1 is available. """
    try:
        return _fullname(_ctx) == 'nodebox.graphics.Context'
    except NameError:
        return False


def _init():
    """
    Autodetect the available drawing backend and initialize the system
    with the correct backend (PyCairo or NodeBox1).
    """
    global _initialized
    if _initialized:
        return

    nodebox = _detect_nodebox()
    if nodebox:
        global _ctx
    else:
        from twyg.cairowrapper import context as _ctx

    twyg.common.init(nodebox=nodebox, ctx=_ctx)

    # Inject the drawing context manually into the modules that need
    # access to the drawing functions (we need to it this way to keep
    # the NodeBox1 compatibility).
    twyg.colorizer._ctx = _ctx
    twyg.common._ctx = _ctx
    twyg.connection._ctx = _ctx
    twyg.node._ctx = _ctx
    twyg.tree._ctx = _ctx

    _initialized = True


def _loadjson(path):
    """ Loads a JSON file. """
    fp = file(path)
    data = json.load(fp)
    # TODO error reporting
    fp.close()
    return data


def _has_levels(section):
    """ Check if a given configuration section has levels or not. """
    # TODO bit of a hack...
    num_dicts = [x for x in section.values() if type(x) == dict]
    return len(num_dicts) == len(section)


def _get_style(section, config):
    """
    Get the style name associated with a given configuration
    section.
    """
    style = get_stylename(section, config)
    del config[STYLE]
    return style


def _create_drawers(config, section, factory_func, constr_args=()):
    """
    Create a list of SectionLevel objects for a given configuration
    section from a full configuration.
    """
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


def buildtree(data_path, config_path, colorscheme_path):
    """
    Build a `Tree` object from a JSON data file according to the rules
    specified in the configuration and apply a colorscheme.

    This method does not perform the actual tree layouting and drawing;
    it stops after creating a ``Tree`` object initialized with the
    correct drawer objects.

    `data_path`
        Path to the JSON data file that describes the tree structure.

    `config_path'
        Path to the configuration file.

    `colorscheme_path`
        Path to the colorscheme file.
    """

    _init()

    data = _loadjson(data_path)
    config = loadconfig(config_path)
    colorscheme = loadconfig(colorscheme_path, flat=True)

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

