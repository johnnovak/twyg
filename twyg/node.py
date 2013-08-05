import math

from twyg.common import textwidth, createpath
from twyg.config import (defaults_path, Properties, StringProperty,
                         NumberProperty, ColorProperty, EnumProperty,
                         BooleanProperty, ArrayProperty)

import twyg.geomutils as geom
import twyg.textwrap as textwrap
from twyg.tree import Direction


LEFT = 'left'
RIGHT = 'right'
CENTER = 'center'
JUSTIFY = 'justify'

DEBUG = False


class NodeDrawer(object):

    def __init__(self, childproperties, defaults, config):
        align = ('auto', 'left', 'right', 'center', 'justify')

        properties = {
            'fontname':               (StringProperty,  {}),
            'fontsizes':              (ArrayProperty,   {'type': NumberProperty}),
            'lineheight':             (NumberProperty,  {'min': 0.0}),
            'textAlign':              (EnumProperty,    {'values': align}),
            'textBaselineCorrection': (NumberProperty,  {}),
            'maxTextWidth':           (NumberProperty,  {'min': 0.0}),
            'hyphenate':              (BooleanProperty, {}),

            'textPadX':               (NumberProperty,  {'min': 0.0}),
            'textPadY':               (NumberProperty,  {'min': 0.0}),

            'strokeWidth':            (NumberProperty,  {'min': 0.0}),

            'nodeDrawShadow':         (BooleanProperty, {}),
            'nodeShadowColor':        (ColorProperty,   {}),
            'nodeShadowBlur':         (NumberProperty,  {'min': 0.0}),
            'nodeShadowOffsX':        (NumberProperty,  {}),
            'nodeShadowOffsY':        (NumberProperty,  {}),

            'drawGradient':           (BooleanProperty, {}),
            'gradientTopColor':       (ColorProperty,   {}),
            'gradientBottomColor':    (ColorProperty,   {})
        }
        properties.update(childproperties)
        self._props = Properties(properties, defaults, config)

        self._wraprect = True

    def _eval_func(self, node):
        if node:
            vars = {
                'depth':       node.depth(),
                'numChildren': len(node.getchildren())
            }
        else:
            vars = {}
        return lambda name: self._props.eval(name, node, vars)

    def precalc_node(self, node):
        """
        Precalculate node properties that are needed by the layout algorithms.
        """

        node.fontsize = self._font_size(node)
        self._precalc_text(node)

        E = self._eval_func(node)

        padx = E('textPadX')
        pady = E('textPadY')

        node.width  = node.textwidth  + padx * 2
        node.height = node.textheight + pady * 2
        node.bboxwidth = node.width
        node.bboxheight = node.height

        node._textxoffs = padx
        node._textyoffs = pady

        node.text_has_background = True

    def connection_point(self, node, direction):
        # TODO make connection point location configurable per node
        # (center, auto, etc)
        if node.isroot():
            x = node.bboxwidth / 2
        else:
            if direction == Direction.Left:
                x = 0
            else:
                x = node.bboxwidth

        y = node.bboxheight / 2
        return node.x + x, node.y + y

    def draw(self, node):
        """
        Draw the node at its (x,y) anchor point. Relies on internal
        properties precalculated by precalc_node.
        """

        E = self._eval_func(node)

        path = self._calc_shape_path(node)

        _ctx.fill(node.fillcolor)
        _ctx.stroke(node.strokecolor)
        _ctx.strokewidth(E('strokeWidth'))

        if E('nodeDrawShadow'):
            _ctx.shadow(dx=E('nodeShadowOffsX'), dy=E('nodeShadowOffsY'),
                        blur=E('nodeShadowBlur'), clr=E('nodeShadowColor'))

        self._draw_gradient_shape(node, path, node.fillcolor)
        self._drawtext(node, node._textxoffs, node._textyoffs)

    def _draw_gradient_shape(self, node, path, basecolor):
        E = self._eval_func(node)

        if E('drawGradient'):
            _ctx.gradientfill(path,
                              E('gradientBottomColor'), E('gradientTopColor'),
                              type='linear')
        else:
            _ctx.fill(basecolor)
            _ctx.drawpath(path)

    def _font_size(self, node):
        """
        Get the font size associated with the node. The font size is
        dependent on the depth of the node.
        """

        E = self._eval_func(node)

        fs = E('fontsizes')
        depth = node.depth()
        idx = depth if depth < len(fs) else -1
        return fs[idx]

    def _precalc_text(self, node):
        E = self._eval_func(node)

        node.fontname       = E('fontname')
        node.lineheight     = E('lineheight')
        node.max_text_width = E('maxTextWidth')
        node.hyphenate      = E('hyphenate')

        _ctx.font(node.fontname, node.fontsize)
        _ctx.lineheight(node.lineheight)

        lineheight = node.lineheight * node.fontsize
        textwidth_func = lambda(txt): textwidth(_ctx, txt,
                                                node.fontname, node.fontsize)

        if self._wraprect:
            (node._textlines, node._textlinewidths, node._textrects,
             node.textwidth,
             node.textheight) = textwrap.wrap_rect(node.label, lineheight,
                                                   textwidth_func,
                                                   node.max_text_width)
        else:
            (node._textlines, node._textlinewidths, node._textrects,
             node.textwidth,
             node.textheight) = textwrap.wrap_shape(node.label, lineheight,
                                                    textwidth_func,
                                                    self._shapefunc,
                                                    hyphenate=node.hyphenate,
                                                    **self._shapefunc_args)

    def _calc_shape_path(self, node):
        raise NotImplementedError

    def _drawtext(self, node, xoffs, yoffs):
        E = self._eval_func(node)

        if not node._textrects:
            return

        # Text alignment
        alignment = LEFT
        text_align = E('textAlign')
        if   text_align == 'right':   alignment = RIGHT
        elif text_align == 'center':  alignment = CENTER
        elif text_align == 'justify': alignment = JUSTIFY
        elif text_align == 'auto':
            if node.isroot():
                alignment = CENTER
            else:
                alignment = (RIGHT if node.direction() == Direction.Left
                             else LEFT)

        # Draw text
        tx = node.x + xoffs
        ty = node.y + yoffs

        baseline_corr = E('textBaselineCorrection')

        _ctx.font(node.fontname, node.fontsize)
        _ctx.lineheight(node.lineheight)

        _ctx.fill(node.fontcolor)

        # TODO make justify_min_lines a config parameter
        justify_min_lines = 5
        ystep = node._textrects[0].h

        nonblank_lines = 0
        for l in node._textlines:
            if l:
                nonblank_lines += 1

        if nonblank_lines <= justify_min_lines:
            self._center_text_vertically(node)

        baseline_offs = node.fontsize * baseline_corr
        lineheight_offs = -(node.lineheight - 1) / 2 * node.fontsize

        if alignment == JUSTIFY and nonblank_lines <= justify_min_lines:
            alignment = CENTER

        if alignment == JUSTIFY:
            spacewidth = textwidth(_ctx, ' ', node.fontname, node.fontsize)

            for i, l in enumerate(node._textlines):
                x, y, w, h = node._textrects[i].params()
                x += tx
                y += ty + baseline_offs + lineheight_offs + ystep

                if DEBUG:
                    _ctx.nofill()
                    _ctx.stroke(node.fontcolor)
                    _ctx.rect(x, y - h, w, h)
                    _ctx.stroke(1, 0, 0)
                    _ctx.nofill()
                    _ctx.rect(tx, ty, node.textwidth, node.textheight)
                    _ctx.fill(node.fontcolor)

                words = l.split()
                numspaces = float(l.count(' '))
                x_spacing = spacewidth
                if numspaces:
                    charswidth = (node._textlinewidths[i]
                                  - numspaces * spacewidth)
                    x_spacing = (w - charswidth) / numspaces

                # TODO remove 7 magic constant
                if ((i == 0 or i == len(node._textlines) - 1)
                    and (x_spacing > spacewidth * 7 or len(words) == 1)):

                    x_spacing = spacewidth
                    x += (w - node._textlinewidths[i]) / 2.

                for w in words:
                    _ctx.text(w, x, y)
                    x += x_spacing + textwidth(_ctx, w,
                                               node.fontname, node.fontsize)
        else:
            for i, l in enumerate(node._textlines):
                x, y, w, h = node._textrects[i].params()
                x += tx
                y += ty + ystep

                if DEBUG:
                    _ctx.nofill()
                    _ctx.stroke(node.fontcolor)
                    _ctx.rect(x, y - h, w, h)
                    _ctx.stroke(1, 0, 0)
                    _ctx.nofill()
                    _ctx.rect(tx, ty, node.textwidth, node.textheight)
                    _ctx.fill(node.fontcolor)

                y += baseline_offs + lineheight_offs

                if alignment == RIGHT:
                    x += w - node._textlinewidths[i]
                elif alignment == CENTER:
                    x += (w - node._textlinewidths[i]) / 2.

                _ctx.text(l, x, y)

    def _center_text_vertically(self, node):
        """
        Shift rects so that the text will appear vertically centered
        within a containing rectangle of the specified height, taking blank
        lines into account as well.

        lines    -- list of strings containing the text in each line
        rects    -- list of equi-height rectangles in [x, y, w, h] format
        height   -- height of the containing rectangle
        """

        if not node._textrects:
            return

        preblanks = 0
        for l in node._textlines:
            if not l:
                preblanks += 1
            else:
                break

        postblanks = 0
        for l in reversed(node._textlines):
            if not l:
                postblanks += 1
            else:
                break

        lineheight = node._textrects[0].h

        numnonblanks = len(node._textlines) - preblanks - postblanks
        textheight = numnonblanks * lineheight
        ystart = (node.textheight - textheight) / 2.
        ystart -= preblanks * lineheight

        yoffs = ystart - node._textrects[0].y

        for r in node._textrects:
            r.y += yoffs


class RectNodeDrawer(NodeDrawer):

    def __init__(self, config={}):
        properties = {
            'roundness':     (NumberProperty, {'min': 0.0, 'max': 1.0}),
            'cornerRadius':  (NumberProperty, {'min': 0.0}),
            'roundingStyle': (EnumProperty,   {'values': ('screen', 'arc')})
        }

        super(RectNodeDrawer, self).__init__(properties,
                                             defaults_path('node/rect.twg'),
                                             config)

    def _calc_shape_path(self, node):
        E = self._eval_func(node)

        style = E('roundingStyle')

        if style == 'screen':
            r =  E('roundness')
            r = min(max(0, r / 2.), 1)

            return _ctx.rect(node.x, node.y, node.width, node.height,
                             roundness=r, draw=False)

        elif style == 'arc':
            r = E('cornerRadius')
            r = min(r, node.height / 2.)
            r = min(r, node.width / 2.)

            points = geom.rounded_rect(node.x, node.y,
                                       node.width, node.height, r)
            return createpath(_ctx, points)


class BoxNodeDrawer(NodeDrawer):

    def __init__(self, config={}):
        orientation = ('topleft', 'topright', 'bottomleft', 'bottomright')

        properties = {
            'boxOrientation':      (EnumProperty,   {'values': orientation}),
            'boxDepth':            (NumberProperty, {'min': 0.0}),
            'boxDepthScaleFactor': (NumberProperty, {'min': 0.0}),
            'horizSideColor':      (ColorProperty,  {}),
            'vertSideColor':       (ColorProperty,  {}),
            'strokeColor':         (ColorProperty,  {})
        }

        super(BoxNodeDrawer, self).__init__(properties,
                                            defaults_path('node/box.twg'),
                                            config)

        # Determine 3D depth orientation
        E = self._eval_func(None)

        orientation = E('boxOrientation')
        self._horiz_dir = 0
        self._vert_dir = 0

        if orientation.find('top') > -1:
            self._vert_dir = 1
        elif orientation.find('bottom') > -1:
            self._vert_dir = -1

        if orientation.find('left') > -1:
            self._horiz_dir = -1
        elif orientation.find('right') > -1:
            self._horiz_dir = 1

        if self._horiz_dir == 0:
            self._horiz_dir = 1

        if self._vert_dir == 0:
            self._vert_dir = 1

    def precalc_node(self, node):
        super(BoxNodeDrawer, self).precalc_node(node)

        E = self._eval_func(node)

        node._boxdepth = (E('boxDepth')
                          * math.pow(E('boxDepthScaleFactor'), node.depth()))

        # Make the bounding box big enough so that the shadow can fit in
        # too -- the actual coordinate calculations will happen later
        node.bboxwidth += node._boxdepth
        node.bboxheight += node._boxdepth

    def draw(self, node):
        """
        Draw the node at its (x,y) anchor point.

        Relies on internal properties precalculated by precalc_node.
        """

        E = self._eval_func(node)

        if E('strokeColor'):
            _ctx.stroke(E('strokeColor'))
            _ctx.strokewidth(E('strokeWidth'))

        d = node._boxdepth

        if self._vert_dir == 1:
            y1 = node.y + d
            y2 = y1 - d
            dv = -d
            oy = y1
        else:
            y1 = node.y + node.height
            y2 = y1 + d
            dv = d
            oy = node.y

        if self._horiz_dir == 1:
            x1 = node.x + node.width
            x2 = x1 + d
            dh = d
            ox = node.x
        else:
            x1 = node.x + d
            x2 = x1 - d
            dh = -d
            ox = x1

        # Draw box
        _ctx.nostroke()
        path = _ctx.rect(ox, oy, node.width, node.height, draw=False)
        self._draw_gradient_shape(node, path, node.fillcolor)

        # Draw 3D depth
        # Draw horizontal side
        _ctx.beginpath(ox, y1)
        _ctx.lineto(ox + node.width, y1)
        _ctx.lineto(ox + node.width + dh, y2)
        _ctx.lineto(ox + dh, y2)
        _ctx.lineto(ox, y1)

        path = _ctx.endpath(draw=False)
        col = E('horizSideColor')
        self._draw_gradient_shape(node, path, col)

        # Draw vertical side
        _ctx.beginpath(x1, oy)
        _ctx.lineto(x1, oy + node.height)
        _ctx.lineto(x2, oy + node.height + dv)
        _ctx.lineto(x2, oy + dv)
        _ctx.lineto(x1, oy)

        path = _ctx.endpath(draw=False)
        col = E('vertSideColor')
        self._draw_gradient_shape(node, path, col)

        tx = node._textxoffs - (node.x - ox)
        ty = node._textyoffs - (node.y - oy)

        self._drawtext(node, tx, ty)


class LineNodeDrawer(NodeDrawer):

    def __init__(self, config={}):
        properties = {
            'maxTextWidth': (NumberProperty, {'min': 0.0})
        }

        super(LineNodeDrawer, self).__init__(properties,
                                             defaults_path('node/line.twg'),
                                             config)

    def precalc_node(self, node):
        """
        Precalculate node properties that are needed by the layout and
        colorizer algorithms.
        """
        super(LineNodeDrawer, self).precalc_node(node)

        node.text_has_background = False

    def draw(self, node):
        E = self._eval_func(node)

        y = node.y + node.height

        _ctx.stroke(node.strokecolor)
        _ctx.strokewidth(E('strokeWidth'))
        _ctx.line(node.x, y, node.x + node.width, y)

        self._drawtext(node, node._textxoffs, node._textyoffs)
        _ctx.nofill()
        _ctx.stroke(1,0,0)
        _ctx.strokewidth(1)

    def connection_point(self, node, direction):
        x = 0 if direction == Direction.Left else node.width
        y = node.height
        return node.x + x, node.y + y


class PolyNodeDrawer(NodeDrawer):

    def __init__(self, config={}):
        properties = {
            'numSides': (NumberProperty, {'min': 0}),
            'rotation': (NumberProperty, {})
        }

        super(PolyNodeDrawer, self).__init__(properties,
                                             defaults_path('node/poly.twg'),
                                             config)

        E = self._eval_func(None)

        self._wraprect = False
        self._shapefunc = geom.calc_regular_polygon_intersections
        self._shapefunc_args = {'numSides': E('numSides'),
                                'rotation': E('rotation')}

    def _calc_shape_path(self, node):
        E = self._eval_func(node)

        r = node.width / 2
        cx = node.x + r
        cy = node.y + node.height / 2

        points = geom.calc_regular_polygon_points(cx, cy, r,
                                                  E('numSides'),
                                                  E('rotation'))
        return createpath(_ctx, points)

    def connection_point(self, node, direction):
        x = node.width / 2
        y = node.height / 2
        return node.x + x, node.y + y


class OvalNodeDrawer(NodeDrawer):

    def __init__(self, config={}):
        properties = {
            'aspectRatio': (NumberProperty, {'min': 0.0}),
            'maxWidth':    (NumberProperty, {'min': 0.0})
        }

        super(OvalNodeDrawer, self).__init__(properties,
                                             defaults_path('node/oval.twg'),
                                             config)

        E = self._eval_func(None)

        self._wraprect = False
        self._shapefunc = geom.calc_ellipse_intersections
        self._shapefunc_args = {'aspectRatio': E('aspectRatio'),
                                'maxWidth':    E('maxWidth')}

    def _calc_shape_path(self, node):
        return _ctx.oval(node.x, node.y, node.width, node.height, draw=False)


class CapsuleNodeDrawer(NodeDrawer):

    def __init__(self, config={}):
        super(CapsuleNodeDrawer, self).__init__({},
                                                defaults_path('node/capsule.twg'),
                                                config)

    def draw(self, node):
        pass


_nodedrawer_map = {
    'rect':    RectNodeDrawer,
    'box':     BoxNodeDrawer,
    'line':    LineNodeDrawer,
    'poly':    PolyNodeDrawer,
    'oval':    OvalNodeDrawer,
    'capsule': CapsuleNodeDrawer
}


def nodedrawer_by_name(name):
    if name in _nodedrawer_map:
        return _nodedrawer_map[name]
    else:
        raise ValueError, 'Unrecognized node drawer name: %s' % name

