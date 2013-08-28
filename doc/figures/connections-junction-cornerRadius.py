import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 635
HEIGHT = 210


config = r"""
[layout]
    style                   layout
    horizontalBalance       0
    rootPadX                80
    nodePadX                80
    nodePadY                10
    branchPadY              10
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
    cornerRadius            %s
    cornerStyle             beveled
    cornerPad               0
    junctionStyle           none
    junctionRadius          14
    junctionXFactor         0.5

[color]
    style               colorizer
    colorscheme         "mint-examples%s"
"""


data = { 'A': ['B', {'C': ['X', 'Y']}, 'D']}

ctx.initsurface(1, 1, OUTFORMAT)
ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, OUTFILE, scale=0.75)
ctx.background(ctx.color(1))

textcol = ctx.color(.3)
ctx.font('Open Sans')

ctx.translate(3, 3)
draw(config % (8, ''), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("cornerRadius = 10", 45, 200)

ctx.translate(350, 0)
draw(config % (1000, 3), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("cornerRadius = 1000", 45, 200)

ctx.writesurface()

