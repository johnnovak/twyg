import math, os

from twyg.common import textwidth, createpath, brightness
from twyg.config import (Properties, StringProperty, NumberProperty,
                         ColorProperty, EnumProperty, BooleanProperty,
                         ArrayProperty)

from twyg.geom import Vector2
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
        anchor = ('auto', 'center')

        properties = {
            'fontName':               (StringProperty,  {}),
            'fontSize':               (NumberProperty,  {'min': 0.0}),
            'lineHeight':             (NumberProperty,  {'min': 0.0}),
            'textAlign':              (EnumProperty,    {'values': align}),
            'justifyMinLines':        (NumberProperty,  {'min': 0.0}),
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

            'textDrawShadow':         (BooleanProperty, {}),
            'textShadowColor':        (ColorProperty,   {}),
            'textShadowOffsX':        (NumberProperty,  {}),
            'textShadowOffsY':        (NumberProperty,  {}),

            'drawGradient':           (BooleanProperty, {}),
            'gradientTopColor':       (ColorProperty,   {}),
            'gradientBottomColor':    (ColorProperty,   {}),

            'connectionAnchorPoint':  (EnumProperty,    {'values': anchor})
        }
        properties.update(childproperties)
        self._props = Properties(properties, self._defaults_path(defaults),
                                 config)
        self._wraprect = True

    # TODO util function in common?
    def _defaults_path(self, conf):
        return os.path.join('node', conf)

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

        E = self._eval_func(node)

        node.fontsize = E('fontSize')
        self._precalc_text(node)

        padx = E('textPadX')
        pady = E('textPadY')

        node.width  = node.textwidth  + padx * 2
        node.height = node.textheight + pady * 2
        node.bboxwidth = node.width
        node.bboxheight = node.height

        node._textxoffs = padx
        node._textyoffs = pady

        node.text_has_background = True

        y = node.bboxheight / 2
        node._conn_point_left = Vector2(0, y)
        node._conn_point_right = Vector2(node.bboxwidth, y)


    def connection_point(self, node, direction):
        E = self._eval_func(node)

        anchor = E('connectionAnchorPoint')

        if anchor == 'auto':
            if direction == Direction.Left:
                p = node._conn_point_left
            else:
                p = node._conn_point_right

            x, y = p.x, p.y

        elif anchor == 'center':
            x = node.bboxwidth / 2
            y = node.bboxheight / 2

        return node.x + x, node.y + y

    def draw(self, node):
        """
        Draw the node at its (x,y) anchor point. Relies on internal
        properties precalculated by precalc_node.
        """

        E = self._eval_func(node)

        path = self._calc_shape_path(node)

        _ctx.push()
        _ctx.translate(node.x, node.y)
        _ctx.fill(node.fillcolor)
        _ctx.stroke(node.strokecolor)
        _ctx.strokewidth(E('strokeWidth'))

        if E('nodeDrawShadow'):
            _ctx.shadow(dx=E('nodeShadowOffsX'), dy=E('nodeShadowOffsY'),
                        blur=E('nodeShadowBlur'), clr=E('nodeShadowColor'))

        self._draw_gradient_shape(node, path, node.fillcolor)
        _ctx.noshadow()

        # Draw text shadow
        if E('textDrawShadow'):
            shadowcolor = E('textShadowColor');
            _ctx.fill(shadowcolor)

            self._drawtext(node, node._textxoffs - E('textShadowOffsX'),
                                 node._textyoffs - E('textShadowOffsY'))

        _ctx.fill(node.fontcolor)
        self._drawtext(node, node._textxoffs, node._textyoffs)

        _ctx.pop()

    def _draw_gradient_shape(self, node, path, basecolor):
        E = self._eval_func(node)

        if E('drawGradient'):
            _ctx.gradientfill(path,
                              E('gradientBottomColor'), E('gradientTopColor'),
                              type='linear')
        else:
            _ctx.fill(basecolor)
            _ctx.drawpath(path)

    def _precalc_text(self, node):
        E = self._eval_func(node)

        node.fontname       = E('fontName')
        node.lineheight     = E('lineHeight')
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
        baseline_corr = E('textBaselineCorrection')

        _ctx.font(node.fontname, node.fontsize)
        _ctx.lineheight(node.lineheight)

        justify_min_lines = E('justifyMinLines')
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
                x += xoffs
                y += yoffs + baseline_offs + lineheight_offs + ystep

                if DEBUG:
                    _ctx.save()
                    _ctx.nofill()
                    _ctx.stroke(node.fontcolor)
                    _ctx.rect(x, y - h, w, h)
                    _ctx.stroke(1, 0, 0)
                    _ctx.rect(tx, ty, node.textwidth, node.textheight)
                    _ctx.restore()

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
                x += xoffs
                y += yoffs + ystep

                if DEBUG:
                    _ctx.save()
                    _ctx.nofill()
                    _ctx.stroke(node.fontcolor)
                    _ctx.rect(x, y - h, w, h)
                    _ctx.stroke(1, 0, 0)
                    _ctx.rect(tx, ty, node.textwidth, node.textheight)
                    _ctx.restore()

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

        super(RectNodeDrawer, self).__init__(properties, 'rect', config)

    def _calc_shape_path(self, node):
        E = self._eval_func(node)

        style = E('roundingStyle')

        if style == 'screen':
            r =  E('roundness')
            r = min(max(0, r / 2.), 1)

            return _ctx.rect(0, 0, node.width, node.height,
                             roundness=r, draw=False)

        elif style == 'arc':
            r = E('cornerRadius')
            r = min(r, node.height / 2.)
            r = min(r, node.width / 2.)

            points = geom.rounded_rect(0, 0, node.width, node.height, r)
            return createpath(_ctx, points, close=False)


class BoxNodeDrawer(NodeDrawer):

    def __init__(self, config={}):
        orientation = ('topleft', 'topright', 'bottomleft', 'bottomright')

        properties = {
            'boxOrientation':      (EnumProperty,   {'values': orientation}),
            'boxDepth':            (NumberProperty, {'min': 0.0}),
            'horizSideColor':      (ColorProperty,  {}),
            'vertSideColor':       (ColorProperty,  {}),
            'strokeColor':         (ColorProperty,  {})
        }

        super(BoxNodeDrawer, self).__init__(properties, 'box', config)

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

        node._boxdepth = E('boxDepth')

        # Make the bounding box big enough so that the shadow can fit in
        # too -- the actual coordinate calculations will happen later
        node.bboxwidth += node._boxdepth
        node.bboxheight += node._boxdepth

        y = node.bboxheight / 2
        node._conn_point_left = Vector2(0, y)
        node._conn_point_right = Vector2(node.bboxwidth, y)

    def draw(self, node):
        """
        Draw the node at its (x,y) anchor point.

        Relies on internal properties precalculated by precalc_node.
        """

        E = self._eval_func(node)
        strokewidth = E('strokeWidth')
        drawstroke = strokewidth > 0

        d = node._boxdepth

        _ctx.push()
        _ctx.translate(node.x, node.y)

        if drawstroke:
            # Set up clip path
            cx1 = cx6 = 0
            cy2 = 0
            cx3 = cx4 = cx1 + node.width + d
            cy5 = cy2 + node.height + d

            if self._vert_dir == self._horiz_dir:
                cy1 = d
                cx2 = d
                cy3 = 0
                cy4 = cy3 + node.height
                cx5 = node.width
                cy6 = cy4 + d

            elif self._vert_dir != self._horiz_dir:
                cy1 = 0
                cx2 = node.width
                cy3 = d
                cy4 = cy3 + node.height
                cx5 = d
                cy6 = cy4 - d

            outline = [
                Vector2(cx1, cy1),
                Vector2(cx2, cy2),
                Vector2(cx3, cy3),
                Vector2(cx4, cy4),
                Vector2(cx5, cy5),
                Vector2(cx6, cy6)
            ]

            offs = geom.offset_poly(outline, strokewidth * .5)
            clippath = createpath(_ctx, offs)

            _ctx.beginclip(clippath)

        # Box drawing stuff
        if drawstroke:
            _ctx.stroke(E('strokeColor'))
            _ctx.strokewidth(strokewidth)
        else:
            _ctx.nostroke()

        if self._vert_dir == 1:
            y1 = d
            y2 = y1 - d
            dv = -d
            oy = y1
        else:
            y1 = node.height
            y2 = y1 + d
            dv = d
            oy = 0

        if self._horiz_dir == 1:
            x1 = node.width
            x2 = x1 + d
            dh = d
            ox = 0
        else:
            x1 = d
            x2 = x1 - d
            dh = -d
            ox = x1

        # Draw box
        path = _ctx.rect(ox, oy, node.width, node.height, draw=False)
        self._draw_gradient_shape(node, path, node.fillcolor)

        # Draw horizontal 3D side
        _ctx.beginpath(ox, y1)
        _ctx.lineto(ox + node.width, y1)
        _ctx.lineto(ox + node.width + dh, y2)
        _ctx.lineto(ox + dh, y2)
        _ctx.lineto(ox, y1)

        path = _ctx.endpath(draw=False)
        col = E('horizSideColor')
        self._draw_gradient_shape(node, path, col)

        # Draw vertical 3D side
        _ctx.beginpath(x1, oy)
        _ctx.lineto(x1, oy + node.height)
        _ctx.lineto(x2, oy + node.height + dv)
        _ctx.lineto(x2, oy + dv)
        _ctx.lineto(x1, oy)

        path = _ctx.endpath(draw=False)
        col = E('vertSideColor')
        self._draw_gradient_shape(node, path, col)

        tx = node._textxoffs + ox
        ty = node._textyoffs + oy

        _ctx.fill(node.fontcolor)
        self._drawtext(node, tx, ty)

        if drawstroke:
            _ctx.endclip()

        _ctx.pop()


class LineNodeDrawer(NodeDrawer):

    def __init__(self, config={}):
        properties = {
            'maxTextWidth': (NumberProperty, {'min': 0.0})
        }

        super(LineNodeDrawer, self).__init__(properties, 'line', config)

    def precalc_node(self, node):
        """
        Precalculate node properties that are needed by the layout and
        colorizer algorithms.
        """
        super(LineNodeDrawer, self).precalc_node(node)

        node.text_has_background = False

        y = node.height
        node._conn_point_left = Vector2(0, y)
        node._conn_point_right = Vector2(node.width, y)

    def draw(self, node):
        E = self._eval_func(node)

        _ctx.push()
        _ctx.translate(node.x, node.y)

        y = node.height

        _ctx.stroke(node.strokecolor)
        _ctx.strokewidth(E('strokeWidth'))
        _ctx.line(0, y, node.width, y)

        _ctx.fill(node.fontcolor)
        self._drawtext(node, node._textxoffs, node._textyoffs)

        _ctx.pop()


class PolyNodeDrawer(NodeDrawer):

    def __init__(self, config={}):
        properties = {
            'numSides': (NumberProperty, {'min': 0}),
            'rotation': (NumberProperty, {})
        }

        super(PolyNodeDrawer, self).__init__(properties, 'poly', config)

        E = self._eval_func(None)

        self._wraprect = False
        self._shapefunc = geom.calc_regular_polygon_intersections
        self._shapefunc_args = {'numSides': int(round(E('numSides'))),
                                'rotation': E('rotation')}

    def precalc_node(self, node):
        super(PolyNodeDrawer, self).precalc_node(node)

        E = self._eval_func(node)

        r = node.width / 2
        cx = r
        cy = node.height / 2

        node._shape_points = geom.calc_regular_polygon_points(
                                   cx, cy, r, int(round(E('numSides'))),
                                   E('rotation'))

        # Slice with a single horizontal line vertically centered to the
        # shape
        connection_points = geom.slice_shape(node._shape_points, cy,
                                             node.height, node.height)

        node._conn_point_left = connection_points[0][0]
        node._conn_point_right = connection_points[0][1]

    def _calc_shape_path(self, node):
        return createpath(_ctx, node._shape_points)


class OvalNodeDrawer(NodeDrawer):

    def __init__(self, config={}):
        properties = {
            'aspectRatio': (NumberProperty, {'min': 0.0}),
            'maxWidth':    (NumberProperty, {'min': 0.0})
        }

        super(OvalNodeDrawer, self).__init__(properties, 'oval', config)

        E = self._eval_func(None)

        self._wraprect = False
        self._shapefunc = geom.calc_ellipse_intersections
        self._shapefunc_args = {'aspectRatio': E('aspectRatio'),
                                'maxWidth':    E('maxWidth')}

    def _calc_shape_path(self, node):
        return _ctx.oval(0, 0, node.width, node.height, draw=False)


# TODO
class CapsuleNodeDrawer(NodeDrawer):

    def __init__(self, config={}):
        super(CapsuleNodeDrawer, self).__init__({}, 'capsule', config)

    def draw(self, node):
        # TODO
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

