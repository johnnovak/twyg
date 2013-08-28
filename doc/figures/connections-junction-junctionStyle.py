import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 625
HEIGHT = 280


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

ctx.initsurface(1, 1, OUTFORMAT)
ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, OUTFILE, scale=0.75)
ctx.background(ctx.color(1))

textcol = ctx.color(.3)
ctx.font('Open Sans')

ctx.translate(3, 3)
draw(config % ('none', 14, ''), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("none", 45, 110)

ctx.push()
ctx.translate(230, 0)
draw(config % ('square', 14, 2), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("square", 45, 110)

ctx.translate(230, 0)
draw(config % ('disc', 14, 3), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("disc", 45, 110)

ctx.pop()
ctx.translate(0, 160)
draw(config % ('diamond', 20, 3), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("diamond", 45, 110)

ctx.writesurface()

