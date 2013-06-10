from twyg.common import scalecolor, createpath
from twyg.config import (CONNECTION_CONFIG, Properties,
                         NumberProperty, EnumProperty)
from twyg.geom import Vector2
from twyg.geomutils import arcpath
from twyg.tree import Direction, opposite_dir


class CurveConnectionDrawer(object):

    def __init__(self, config={}):
        properties = {
            'rootLineWidthStart': (NumberProperty, {'min': 0.0}),
            'nodeLineWidthStart': (NumberProperty, {'min': 0.0}),
            'rootLineWidthEnd':   (NumberProperty, {'min': 0.0}),
            'nodeLineWidthEnd':   (NumberProperty, {'min': 0.0}),
            'rootCx1Factor':      (NumberProperty, {}),
            'nodeCx1Factor':      (NumberProperty, {}),
            'nodeCx2Factor':      (NumberProperty, {}),
            'nodeCy1Factor':      (NumberProperty, {}),
            'nodeCy2Factor':      (NumberProperty, {})
        }

        defaults = 'defaults/connection/curve.twg'
        self._props = Properties(properties, defaults, config)

    def _eval_func(self, node):
        return lambda name: self._props.eval(name, node)

    def draw(self, node):
        """
        Draw a curved connection between a node and its child nodes.
        """

        E = self._eval_func(node)

        if node.isleaf():
            return

        # TODO necessary?
        _ctx.autoclosepath(True)
        _ctx.stroke(node.connectioncolor)
        _ctx.fill(node.connectioncolor)

        children = node.children

        for child in children:
            # TODO remove when levels are introduced
            if node.isroot():
                linewidth = E('rootLineWidthEnd')
            else:
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

                if node.isroot():
                    startwidth = linewidth - E('rootLineWidthStart')
                else:
                    startwidth = E('nodeLineWidthStart') - 1

                # TODO remove isroot stuff when levels are introduced
                if not node.isroot():
                    sw = startwidth / 2.

                    _ctx.beginpath(x1, y1 - sw)
                    _ctx.curveto(x1 + cx1, y1 + cy1, x2 - cx2, y2 - cy2, x2, y2)
                    _ctx.curveto(x2 - cx2, y2 - cy2, x1 + cx1, y1 + cy1, x1, y1 + sw)
                    _ctx.endpath()

                else:
                    cx1 *= E('rootCx1Factor')
                    sw = startwidth * 2.

                    _ctx.beginpath(x1 - sw, y1)
                    _ctx.curveto(x1, y1, x2 - cx1, y2, x2, y2)
                    _ctx.curveto(x2 - cx1, y2, x1, y1, x1 + sw, y1)
                    _ctx.endpath()


class JunctionConnectionDrawer(object):

    def __init__(self, config={}):
        corner_styles = ('square', 'beveled', 'rounded')
        junction_styles = ('square', 'disc', 'diamond')
        junction_sign = ('none', 'plus', 'minus')

        properties = {
            'linewidth':           (NumberProperty, {'min': 0.0}),
            'junctionXFactor':     (NumberProperty, {}),
            'cornerStyle':         (EnumProperty,   {'values': corner_styles}),
            'cornerRadius':        (NumberProperty, {'min': 0.0}),
            'junctionStyle':       (EnumProperty,   {'values': junction_styles}),
            'junctionRadius':      (NumberProperty, {'min': 0.0}),
            'junctionStrokeWidth': (NumberProperty, {'min': 0.0}),
            'junctionSign':        (EnumProperty,   {'values': junction_sign}),
            'junctionSignSize':    (NumberProperty, {'min': 0.0}),
            'junctionSignStrokeWidth': (NumberProperty, {'min': 0.0})
        }

        defaults = 'defaults/connection/junction.twg'
        self._props = Properties(properties, defaults, config)

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

        linewidth = E('linewidth')

        # TODO necessary?
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

        # First (top) corner radius
        r = min(E('cornerRadius'), abs(jx - xfirst))
        r1 = min(r, abs(yfirst - jy))
        if ysecond < jy:
            r1 = min(r, abs(yfirst - ysecond))

        # Last (bottom) corner radius
        r2 = min(r, abs(ylast - jy))
        if ypenultimate > jy:
            r2 = min(r, abs(ylast - ypenultimate))

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

        path = createpath(_ctx, segments)
        _ctx.drawpath(path)

        # Draw junction point
        style = E('junctionStyle')
        if style == 'none':
            return

        r = E('junctionRadius')
        r2 = r / 2.

        _ctx.strokewidth(E('junctionStrokeWidth'))

        # TODO junctionFillColor
        _ctx.fill(node.connectioncolor)

        # TODO junctionStrokeColor
        #_ctx.stroke( )
        _ctx.stroke(node.connectioncolor)

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

        d = E('junctionSignSize') / 2.
        _ctx.strokewidth(E('junctionSignStrokeWidth'))

        # TODO junctionSignColor
        _ctx.stroke(1)

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

