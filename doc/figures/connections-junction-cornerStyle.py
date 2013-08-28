import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 625
HEIGHT = 160


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
    cornerStyle             %s
    junctionStyle           disc
    junctionRadius          14
    junctionXFactor         0.5

[color]
    style               colorizer
    colorscheme         "mint-examples%s"
"""


data = { 'A': ['B', 'C', 'D']}

ctx.initsurface(1, 1, OUTFORMAT)
ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, OUTFILE, scale=0.75)
ctx.background(ctx.color(1))

textcol = ctx.color(.3)
ctx.font('Open Sans')

ctx.translate(3, 3)
draw(config % ('square', ''), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("square", 45, 150)

ctx.translate(230, 0)
draw(config % ('beveled', 2), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("beveled", 45, 150)

ctx.translate(230, 0)
draw(config % ('rounded', 3), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("rounded", 45, 150)

ctx.writesurface()

