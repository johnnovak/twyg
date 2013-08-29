import os, sys

from fig import *
from twyg.cairowrapper import context as ctx


def drawconn(ctx, linewidth_start, linewidth_end, x1, y1, x2, y2,
             cx1, cx2, cy1, cy2):
    ctx.strokewidth(linewidth_end)

    x2 -= linewidth_end / 2

    cx1 = (x2 - x1) * cx1
    cx2 = (x2 - x1) * cx2

    cy1 = (y2 - y1) * cy1
    cy2 = (y2 - y1) * cy2

    startwidth = linewidth_start - 1
    sw = startwidth / 2.

    p1x = x1 + cx1
    p1y = y1 + cy1

    p2x = x2 - cx2
    p2y = y2 - cy2

    ctx.beginpath(x1, y1 - sw)
    ctx.curveto(p1x, p1y, p2x, p2y, x2, y2)
    ctx.curveto(p2x, p2y, p1x, p1y, x1, y1 + sw)
    ctx.endpath()

    ctx.nostroke()
    ctx.fill(1, 0, 0)
    ctx.oval(p1x - 3, p1y - 3, 6, 6)

    ctx.fill(0, 1, 0)
    ctx.oval(p2x - 3, p2y - 3, 6, 6)


init_surface(500, 150, scale=0.8)
ctx.background(ctx.color(1))

ctx.stroke(.3)
ctx.fill(.3)
#drawconn(ctx, 20, 3,
#         20, 20, 250, 120,
#         0.7, 0.28, 0.1, 0.2)

drawconn(ctx, 3, 3,
         20, 20, 250, 120,
         0.2, 0, 1.0, 0.0)

ctx.writesurface()

