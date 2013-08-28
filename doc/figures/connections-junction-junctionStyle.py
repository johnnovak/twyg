import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
WIDTH = 165
HEIGHT = 80


config = r"""
[layout]
    style                   layout
    horizontalBalance       0
    rootPadX                80
    nodePadX                80
    radialMinNodes          1000
    sameWidthSiblings       no
    snapParentToChildren    yes

[node]
    style                   rect
    fontName                "Open Sans"
    fontSize                17
    strokeWidth             3
    roundingStyle           arc
    cornerRadius            5
    textPadX                14
    textPadY                5
    textBaselineCorrection  -0.15

[connection]
    style                   junction 
    lineWidth               4
    cornerRadius            20
    cornerStyle             rounded
    junctionStyle           %s
    junctionRadius          %s
    junctionXFactor         0.5

[color]
    style               colorizer
    colorscheme         "mint-examples%s"
"""


data = { 'A': ['B', 'C']}

scale = 0.75

ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, imgname(OUTFORMAT, '-a'), scale=scale)
ctx.background(ctx.color(1))
ctx.translate(3, 3)
draw(config % ('none', 14, ''), data)
ctx.writesurface()

ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, imgname(OUTFORMAT, '-b'), scale=scale)
ctx.background(ctx.color(1))
ctx.translate(3, 3)
draw(config % ('square', 14, 2), data)
ctx.writesurface()

ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, imgname(OUTFORMAT, '-c'), scale=scale)
ctx.background(ctx.color(1))
ctx.translate(3, 3)
draw(config % ('disc', 14, 3), data)
ctx.writesurface()

ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, imgname(OUTFORMAT, '-d'), scale=scale)
ctx.background(ctx.color(1))
ctx.translate(3, 3)
draw(config % ('diamond', 20, 3), data)
ctx.writesurface()

