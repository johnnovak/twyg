import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
WIDTH = 280
HEIGHT = 176


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

[connection]
    style                   junction 
    lineWidth               3
    cornerRadius            20
    cornerStyle             rounded
    junctionStyle           square
    junctionRadius          12
    junctionFillColor       color.red
    junctionStrokeColor     color.red
    junctionXFactor         %s


[color]
    style               colorizer
    colorscheme         "mint-examples"
    connectionColor     #ea3
"""


data = { '1': [{'2': ['3', '4']}, '5', '6']}

scale = 0.75

ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, imgname(OUTFORMAT, '-a'), scale=scale)
ctx.background(ctx.color(1))
ctx.translate(3, 3)
draw(config % 0.0, data)
ctx.writesurface()

ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, imgname(OUTFORMAT, '-b'), scale=scale)
ctx.background(ctx.color(1))
ctx.translate(3, 3)
draw(config % 0.5, data)
ctx.writesurface()

ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, imgname(OUTFORMAT, '-c'), scale=scale)
ctx.background(ctx.color(1))
ctx.translate(3, 3)
draw(config % 1.0, data)
ctx.writesurface()


