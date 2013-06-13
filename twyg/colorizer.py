from twyg.common import scalecolor
from twyg.config import (COLOR_CONFIG, Properties, NumberProperty,
                         ColorProperty, ArrayProperty)

from twyg.css3colors import color_to_rgba


class Colorizer(object):

    def __init__(self, config, colorscheme):
        properties = {
            # TODO delete
#            'boxDepthMin': (NumberProperty, {'min': 0.0}),
#            'boxDepthMax': (NumberProperty, {'min': 0.0}),
            'fillColor':   (ColorProperty, {}),
            'strokeColor': (ColorProperty, {}),
            'fontColor':   (ColorProperty, {})
        }

        colorscheme_properties = {
            'backgroundColor': (ColorProperty, {}),
            'rootColor':       (ColorProperty, {}),
            'nodeColors':      (ArrayProperty, {'type': ColorProperty})
        }

        self._props = Properties(properties,
                                 'defaults/colorizer/colorizer.twg', config)

        self._colorscheme_props = Properties(
                colorscheme_properties, 'defaults/colorizer/colorscheme.twg',
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

        if node.isroot():
            node.basecolor = C('rootColor')
        elif node.isleaf():
            node.basecolor = node.parent.basecolor
        else:
            nodecolors = C('nodeColors')
            node.basecolor = nodecolors[self._colorindex]
            self._colorindex = (self._colorindex + 1) % len(nodecolors)

            if node.parent.basecolor == node.basecolor:
                self.colorize(node)

        E = self._eval_func(node)

        node.fontcolor = E('fontColor')

        # TODO remove when levels are introduced
        if node.isroot():
            node.basecolor = C('rootColor')
            node.fillcolor = node.basecolor
            node.strokecolor = node.basecolor
            node.connectioncolor = node.basecolor
        else:
            node.fillcolor = E('fillColor')
            node.strokecolor = E('strokeColor')
            # TODO connection color property
            node.connectioncolor = node.basecolor

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

