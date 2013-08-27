import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 670
HEIGHT = 520


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

ctx.initsurface(1, 1, OUTFORMAT)
ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, OUTFILE, scale=0.7)
ctx.background(ctx.color(1))

textcol = ctx.color(.3)
ctx.font('Open Sans')

ctx.translate(3, 3)
draw(config % 0.0, data)
ctx.fill(textcol)
ctx.fontsize(20)
ctx.text("junctionXFactor = 0.0", 65, 210)

ctx.push()
ctx.translate(340, 0)
draw(config % 0.5, data)
ctx.fill(textcol)
ctx.fontsize(20)
ctx.text("junctionXFactor = 0.5", 65, 210)

ctx.pop()
ctx.translate(0, 280)
draw(config % 1.0, data)
ctx.fill(textcol)
ctx.fontsize(20)
ctx.text("junctionXFactor = 1.0", 65, 210)

ctx.writesurface()

