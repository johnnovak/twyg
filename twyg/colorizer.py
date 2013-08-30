from twyg.common import brightness
from twyg.config import (colors_path, Properties,
                         BooleanProperty, NumberProperty, ColorProperty,
                         ArrayProperty, StringProperty, loadconfig)


class Colorizer(object):

    def __init__(self, config, colorscheme_path=None):
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

        self._props = Properties(properties, 'colorizer/cycle.twg', config)

        E = self._eval_func()
        if not colorscheme_path:
            colorscheme_path = E('colorscheme')

        colorscheme = loadconfig(colors_path(colorscheme_path), flat=True)

        self._colorscheme_props = Properties(
                colorscheme_properties, 'colorizer/colorscheme.twg', colorscheme)

        self._colorindex = 0

    def _eval_func(self, node=None):
        if node:
            vars = {
                'bgColor': self.background_color(),
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

        self._props = Properties(properties, 'colorizer/cycle.twg', config)

        E = self._eval_func()
        if not colorscheme_path:
            colorscheme_path = E('colorscheme')

        colorscheme = loadconfig(colors_path(colorscheme_path), flat=True)

        self._colorscheme_props = Properties(
                colorscheme_properties, 'colorizer/colorscheme.twg', colorscheme)

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


_colorizer_map = {
    'cycle': CycleColorizer
}


def colorizer_by_name(name):
    if name in _colorizer_map:
        return _colorizer_map[name]
    else:
        raise ValueError, 'Unrecognized colorizer name: %s' % name

