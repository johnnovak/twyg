from twyg.common import brightness
from twyg.config import (defaults_path, Properties, BooleanProperty,
                         NumberProperty, ColorProperty, ArrayProperty)


class Colorizer(object):

    def __init__(self, config, colorscheme):
        properties = {
            'fillColor':          (ColorProperty,   {}),
            'strokeColor':        (ColorProperty,   {}),
            'connectionColor':    (ColorProperty,   {}),
            'fontColor':          (ColorProperty,   {}),
            'fontColorAuto':      (BooleanProperty, {}),
            'fontColorAutoDark':  (ColorProperty,   {}),
            'fontColorAutoLight': (ColorProperty,   {})
        }

        colorscheme_properties = {
            'backgroundColor': (ColorProperty, {}),
            'rootColor':       (ColorProperty, {}),
            'nodeColors':      (ArrayProperty, {'type': ColorProperty})
        }

        self._props = Properties(properties,
                                 defaults_path('colorizer/colorizer.twg'),
                                 config)

        self._colorscheme_props = Properties(
                colorscheme_properties,
                defaults_path('colorizer/colorscheme.twg'),
                colorscheme)

        self._colorindex = 0

    def _eval_func(self, node):
        vars = {
            'bgColor': self.background_color(),
        }
        return lambda name: self._props.eval(name, node, vars)

    def colorize(self, node):
        """
        Set the color of a node by cycling through all available colors.
        Leaves have the same color as their parent.
        """

        C = self._colorscheme_props.eval

        node.bgcolor = self.background_color()

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

        E = self._eval_func(node)

        node.fillcolor = E('fillColor')
        node.strokecolor = E('strokeColor')
        node.connectioncolor = E('connectionColor')

        # Determine font color
        if E('fontColorAuto'):
            text_bgcolor = (node.fillcolor if node.text_has_background
                                           else self.background_color())
            textcolor = node.fillcolor

            if abs(brightness(text_bgcolor) - brightness(textcolor)) < .3:
                textcolor_dark  = E('fontColorAutoDark')
                textcolor_light = E('fontColorAutoLight')

                b = brightness(text_bgcolor)

                if (  abs(b - brightness(textcolor_dark))
                    > abs(b - brightness(textcolor_light))):
                    textcolor = textcolor_dark
                else:
                    textcolor = textcolor_light

            node.fontcolor = textcolor
        else:
            node.fontcolor = E('fontColor')

    def background_color(self):
        C = self._colorscheme_props.eval
        return C('backgroundColor')


_colorizer_map = {
    'colorizer': Colorizer
}


def colorizer_by_name(name):
    if name in _colorizer_map:
        return _colorizer_map[name]
    else:
        raise ValueError, 'Unrecognized colorizer name: %s' % name

