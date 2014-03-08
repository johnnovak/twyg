import os

from twyg.common import createpath
from twyg.config import (Properties, NumberProperty,
                         EnumProperty, ColorProperty)

from twyg.geom import Vector2
from twyg.geomutils import arcpath
from twyg.tree import Direction, opposite_dir


# TODO util function in common?
def defaults_path(conf):
    return os.path.join('connection', conf)


class CurveConnectionDrawer(object):

    def __init__(self, config={}):
        properties = {
            'nodeLineWidthStart': (NumberProperty, {'min': 0.0}),
            'nodeLineWidthEnd':   (NumberProperty, {'min': 0.0}),
            'nodeCx1Factor':      (NumberProperty, {}),
            'nodeCx2Factor':      (NumberProperty, {}),
            'nodeCy1Factor':      (NumberProperty, {}),
            'nodeCy2Factor':      (NumberProperty, {})
        }

        self._props = Properties(properties, defaults_path('curve'), config)

    def _eval_func(self, node):
        return lambda name: self._props.eval(name, node)

    def draw(self, node):
        """
        Draw a curved connection between a node and its child nodes.
        """

        E = self._eval_func(node)

        if node.isleaf():
            return

        _ctx.autoclosepath(True)
        _ctx.stroke(node.connectioncolor)
        _ctx.fill(node.connectioncolor)

        children = node.children

        for child in children:
            linewidth = E('nodeLineWidthEnd')

            _ctx.strokewidth(linewidth)

            direction = child.direction()
            opp_direction = opposite_dir(direction)

            x1, y1 = node.connection_point(direction)
            x2, y2 = child.connection_point(opp_direction)

            if direction == Direction.Left:
                x2 -= linewidth / 2
            elif direction == Direction.Right:
                x2 += linewidth / 2

            if len(children) == 1:
                _ctx.line(x1, y1, x2, y2)
            else:
                cx1 = (x2 - x1) * E('nodeCx1Factor')
                cx2 = (x2 - x1) * E('nodeCx2Factor')

                cy1 = (y2 - y1) * E('nodeCy1Factor')
                cy2 = (y2 - y1) * E('nodeCy2Factor')

                p1x = x1 + cx1
                p1y = y1 + cy1
                p2x = x2 - cx2
                p2y = y2 - cy2

                startwidth = E('nodeLineWidthStart') - 1
                sw = startwidth / 2.

                _ctx.beginpath(x1, y1 - sw)
                _ctx.curveto(p1x, p1y, p2x, p2y, x2, y2)
                _ctx.curveto(p2x, p2y, p1x, p1y, x1, y1 + sw)
                _ctx.endpath()


class JunctionConnectionDrawer(object):

    def __init__(self, config={}):
        corner_styles = ('square', 'beveled', 'rounded')
        junction_styles = ('none', 'square', 'disc', 'diamond')
        junction_sign = ('none', 'plus', 'minus')

        properties = {
            'lineWidth':        (NumberProperty, {'min': 0.0}),
            'junctionXFactor':  (NumberProperty, {}),

            'cornerStyle':      (EnumProperty, {'values': corner_styles}),
            'cornerRadius':     (NumberProperty, {'min': 0.0}),
            'cornerPad':        (NumberProperty, {'min': 0.0}),

            'junctionStyle':    (EnumProperty,{'values': junction_styles}),

            'junctionRadius':       (NumberProperty, {'min': 0.0}),
            'junctionFillColor':    (ColorProperty,  {}),
            'junctionStrokeWidth':  (NumberProperty, {'min': 0.0}),
            'junctionStrokeColor':  (ColorProperty,  {}),

            'junctionSign':             (EnumProperty,
                                        {'values': junction_sign}),

            'junctionSignSize':         (NumberProperty, {'min': 0.0}),
            'junctionSignStrokeWidth':  (NumberProperty, {'min': 0.0}),
            'junctionSignColor':        (ColorProperty,  {})
        }

        self._props = Properties(properties, defaults_path('junction'),
                                 config)

    def _eval_func(self, node):
        return lambda name: self._props.eval(name, node)

    def draw(self, node):
        if node.isroot():
            self._draw(node, Direction.Left)
            self._draw(node, Direction.Right)
        else:
            self._draw(node)

    def _draw(self, node, direction=None):
        """
        Draw a curved connection between a node and its child nodes.
        """

        E = self._eval_func(node)

        children = node.getchildren(direction)
        if not children:
            return

        linewidth = E('lineWidth')

        _ctx.autoclosepath(True)
        _ctx.stroke(node.connectioncolor)
        _ctx.fill(node.connectioncolor)
        _ctx.strokewidth(linewidth)

        firstchild = children[0]
        lastchild = children[-1]

        direction = firstchild.direction()
        opp_direction = opposite_dir(direction)
        x1, y1 = node.connection_point(direction)
        xfirst, yfirst = firstchild.connection_point(opp_direction)

        # Special case: draw straight line if there's only one child
        if len(children) == 1:
            _ctx.line(x1, y1, xfirst, yfirst)
            return

        # Calculate junction point position
        jx = x1 + (xfirst - x1) * E('junctionXFactor')
        jy = y1

        # Draw line from parent node to junction point
        _ctx.line(x1, y1, jx, jy)

        # Limit first & last corner radius to the available area
        ylast = lastchild.connection_point(opp_direction)[1]
        ysecond = children[1].connection_point(opp_direction)[1]
        ypenultimate = children[-2].connection_point(opp_direction)[1]

        # Starting corner radius
        cornerPad = E('cornerPad')
        r = min(E('cornerRadius'), abs(jx - xfirst) - cornerPad)
        r = max(r, 0)

        # Adjusted first (top) corner radius
        r1 = min(r, abs(yfirst - jy) - cornerPad)
        r1 = max(r1, 0)
        if ysecond < jy:
            r1 = min(r, abs(yfirst - ysecond) - cornerPad)
            r1 = max(r1, 0)

        # Adjusted last (bottom) corner radius
        r2 = min(r, abs(ylast - jy) - cornerPad)
        r2 = max(r2, 0)
        if ypenultimate > jy:
            r2 = min(r, abs(ylast - ypenultimate) - cornerPad)
            r2 = max(r2, 0)

        # Draw main branch as a single path to ensure line continuity
        p1 = Vector2(jx, yfirst + r1)
        p2 = Vector2(jx, ylast - r2)
        segments = [[p1, p2]]

        corner_style = E('cornerStyle')

        for i, child in enumerate(children):
            direction = child.direction()
            opp_direction = opposite_dir(direction)

            x2, y2 = child.connection_point(opp_direction)
            if direction == Direction.Left:
                x2 -= linewidth / 2
            elif direction == Direction.Right:
                x2 += linewidth / 2

            # Draw corners
            if direction == Direction.Left:
                a1 = 90
                da = -90
                dx1 = r1 * 2
                dx2 = r2 * 2
            else:
                a1 = da = 90
                dx1 = dx2 = 0

            x1 = jx
            if child is firstchild:
                x1 += -r1 if direction == Direction.Left else r1

                if (corner_style == 'square' or abs(y2 - jy) < .001):
                    p1 = Vector2(jx, y2)
                    p2 = Vector2(jx, y2 + r1)
                    segments.insert(0, [p1, p2])

                    p1 = Vector2(x1, y2)
                    p2 = Vector2(jx, y2)
                    segments.insert(0, [p1, p2])

                elif corner_style == 'beveled':
                    p1 = Vector2(x1, y2)
                    p2 = Vector2(jx, y2 + r1)
                    segments.insert(0, [p1, p2])

                elif corner_style == 'rounded':
                    arc = arcpath(jx - dx1, y2, r1 * 2, r1 * 2, a1, da)
                    segments = arc + segments

                p1 = Vector2(x2, y2)
                p2 = Vector2(x1, y2)
                segments.insert(0, [p1, p2])

            elif child is lastchild:
                x1 += -r2 if direction == Direction.Left else r2

                if (corner_style == 'square' or abs(y2 - jy) < .001):
                    p1 = Vector2(jx, y2 - r2)
                    p2 = Vector2(jx, y2)
                    segments.append([p1, p2])

                    p1 = Vector2(jx, y2)
                    p2 = Vector2(x1, y2)
                    segments.append([p1, p2])

                elif corner_style == 'beveled':
                    p1 = Vector2(jx, y2 - r2)
                    p2 = Vector2(x1, y2)
                    segments.append([p1, p2])

                elif corner_style == 'rounded':
                    arc = arcpath(jx - dx2, y2 - r2 * 2, r2 * 2, r2 * 2,
                                  a1 + da, da)
                    segments = segments + arc

                p1 = Vector2(x1, y2)
                p2 = Vector2(x2, y2)
                segments.append([p1, p2])

            else:
                _ctx.line(x1, y2, x2, y2)

        # Draw main branch path
        _ctx.nofill()

        path = createpath(_ctx, segments, close=False)
        _ctx.drawpath(path)

        # Draw junction point
        style = E('junctionStyle')
        if style == 'none':
            return

        r = E('junctionRadius')
        r2 = r / 2.

        _ctx.fill(E('junctionFillColor'))
        _ctx.stroke(E('junctionStrokeColor'))
        _ctx.strokewidth(E('junctionStrokeWidth'))

        if style == 'square':
            _ctx.rect(jx - r2, jy - r2, r, r)

        elif style == 'disc':
            _ctx.oval(jx - r2, jy - r2, r, r)

        elif style == 'diamond':
            _ctx.beginpath(jx, jy - r2)
            _ctx.lineto(jx + r2, jy)
            _ctx.lineto(jx, jy + r2)
            _ctx.lineto(jx - r2, jy)
            _ctx.lineto(jx, jy - r2)
            _ctx.endpath()

        # Draw junction sign
        sign = E('junctionSign')
        if sign == 'none':
            return

        _ctx.stroke(E('junctionSignColor'))

        d = E('junctionSignSize') / 2.
        _ctx.strokewidth(E('junctionSignStrokeWidth'))

        if sign in ('minus', 'plus'):
            _ctx.line(jx - d, jy, jx + d, jy)

        if sign == 'plus':
            _ctx.line(jx, jy - d, jx, jy + d)


_conndrawer_map = {
    'curve':    CurveConnectionDrawer,
    'junction': JunctionConnectionDrawer
}


def conndrawer_by_name(name):
    if name in _conndrawer_map:
        return _conndrawer_map[name]
    else:
        raise ValueError, 'Unrecognized connection drawer name: %s' % name

