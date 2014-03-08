import os

from twyg.common import brightness
from twyg.config import (colors_path, Properties,
                         BooleanProperty, NumberProperty, ColorProperty,
                         ArrayProperty, StringProperty, loadconfig)


class Colorizer(object):

    def __init__(self, childproperties, defaults, config,
                 colorscheme_path=None):

        properties = {
            'colorscheme':            (StringProperty,  {}),
            'fillColor':              (ColorProperty,   {}),
            'strokeColor':            (ColorProperty,   {}),
            'connectionColor':        (ColorProperty,   {}),
            'fontColor':              (ColorProperty,   {}),
            'fontColorAuto':          (BooleanProperty, {}),
            'fontColorAutoDark':      (ColorProperty,   {}),
            'fontColorAutoLight':     (ColorProperty,   {}),
            'fontColorAutoThreshold': (NumberProperty,  {'min': 0.0})
        }

        colorscheme_properties = {
            'backgroundColor': (ColorProperty, {}),
            'rootColor':       (ColorProperty, {}),
            'nodeColors':      (ArrayProperty, {'type': ColorProperty})
        }
        properties.update(childproperties)
        self._props = Properties(properties, self._defaults_path(defaults),
                                 config)

        E = self._eval_func()
        if not colorscheme_path:
            colorscheme_path = E('colorscheme')

        colorscheme = loadconfig(colors_path(colorscheme_path), flat=True)

        self._colorscheme_props = Properties(colorscheme_properties,
                                             'colorizer/colorscheme',
                                             colorscheme)

    # TODO util function in common?
    def _defaults_path(self, conf):
        return os.path.join('colorizer', conf)

    def _eval_func(self, node=None):
        # TODO duplicate from node.py
        if node:
            vars = {
                'depth':       node.depth(),
                'numChildren': len(node.getchildren()),
                'bgColor':     self.background_color()
            }
        else:
            vars = {}
        return lambda name: self._props.eval(name, node, vars)

    def colorize(self, node):
        C = self._colorscheme_props.eval

        node.bgcolor = self.background_color()
        self._set_basecolor(node)

        E = self._eval_func(node)

        node.fillcolor = E('fillColor')
        node.strokecolor = E('strokeColor')
        node.connectioncolor = E('connectionColor')

        # Determine font color
        if E('fontColorAuto'):
            node.fontcolor = self._calc_auto_textcolor(node)
        else:
            node.fontcolor = E('fontColor')

    def background_color(self):
        C = self._colorscheme_props.eval
        return C('backgroundColor')

    def _calc_auto_textcolor(self, node):
        E = self._eval_func(node)

        text_bgcolor = (node.fillcolor if node.text_has_background
                                       else self.background_color())
        textcolor = node.fillcolor

        if abs(  brightness(text_bgcolor)
               - brightness(textcolor)) < E('fontColorAutoThreshold'):
            textcolor_dark  = E('fontColorAutoDark')
            textcolor_light = E('fontColorAutoLight')

            b = brightness(text_bgcolor)

            if (  abs(b - brightness(textcolor_dark))
                > abs(b - brightness(textcolor_light))):
                textcolor = textcolor_dark
            else:
                textcolor = textcolor_light

        return textcolor

    def _set_basecolor(self, node):
        raise NotImplementedError


class CycleColorizer(Colorizer):

    def __init__(self, config, colorscheme_path=None):
        properties = {}

        super(CycleColorizer, self).__init__(
            properties, 'cycle', config,
            colorscheme_path=colorscheme_path)

        self._colorindex = 0

    def _set_basecolor(self, node):
        """
        Set the color of a node by cycling through all available colors.
        Leaves have the same color as their parent.
        """

        C = self._colorscheme_props.eval

        if node.isroot():
            node.basecolor = C('rootColor')
        elif node.isleaf():
            node.basecolor = node.parent.basecolor
        else:
            nodecolors = C('nodeColors')
            node.basecolor = nodecolors[self._colorindex]

            if len(nodecolors) > 1:
                self._colorindex = (self._colorindex + 1) % len(nodecolors)
                if node.parent.basecolor == node.basecolor:
                    self.colorize(node)


class DepthColorizer(Colorizer):

    def __init__(self, config, colorscheme_path=None):
        properties = {}

        super(DepthColorizer, self).__init__(
            properties, 'depth', config,
            colorscheme_path=colorscheme_path)

    def _set_basecolor(self, node):
        """
        Set the color of a node by cycling through all available colors.
        Leaves have the same color as their parent.
        """

        C = self._colorscheme_props.eval

        if node.isroot():
            node.basecolor = C('rootColor')
        else:
            nodecolors = C('nodeColors')
            node.basecolor = nodecolors[node.depth() % len(nodecolors)]


class BranchColorizer(Colorizer):

    def __init__(self, config, colorscheme_path=None):
        properties = {}

        super(BranchColorizer, self).__init__(
            properties, 'branch', config,
            colorscheme_path=colorscheme_path)

        self._colorindex = 0

    def _set_basecolor(self, node):
        """
        Set the color of a node by cycling through all available colors.
        Leaves have the same color as their parent.
        """

        C = self._colorscheme_props.eval

        if node.isroot():
            node.basecolor = C('rootColor')
        elif node.depth() == 1:
            nodecolors = C('nodeColors')
            self._colorindex = (self._colorindex + 1) % len(nodecolors)
            node.basecolor = nodecolors[self._colorindex]
        else:
            node.basecolor = node.parent.basecolor


_colorizer_map = {
    'cycle': CycleColorizer,
    'depth': DepthColorizer,
    'branch': BranchColorizer
}


def colorizer_by_name(name):
    if name in _colorizer_map:
        return _colorizer_map[name]
    else:
        raise ValueError, 'Unrecognized colorizer name: %s' % name

