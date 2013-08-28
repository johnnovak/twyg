import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 625
HEIGHT = 120


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
    junctionStyle           disc
    junctionRadius          22
    junctionSign            %s
    junctionSignStrokeWidth 3.2
    junctionSignSize        12
    junctionXFactor         0.5
    junctionSignColor       #fff

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
draw(config % ('none', ''), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("none", 45, 110)

ctx.push()
ctx.translate(230, 0)
draw(config % ('plus', 2), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("plus", 45, 110)

ctx.translate(230, 0)
draw(config % ('minus', 3), data)
ctx.fill(textcol)
ctx.fontsize(18)
ctx.text("minus", 45, 110)

ctx.writesurface()

