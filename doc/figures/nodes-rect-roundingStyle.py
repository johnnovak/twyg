import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 370
HEIGHT = 60


config1 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               rect
    strokeWidth         3
    roundingStyle       screen

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples3"
    fontColorAuto       no
    fontColor           #fff
"""

config2 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               rect
    strokeWidth         3
    roundingStyle       arc
    cornerRadius        25

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples3"
    fontColorAuto       no
    fontColor           #fff
"""


data1 = { 'style = screen': [] }
data2 = { 'style = arc': [] }


ctx.initsurface(1, 1, OUTFORMAT)
ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, OUTFILE, scale=0.7)
ctx.background(ctx.color(1))

ctx.translate(7, 7)
draw(config1, data1)

ctx.translate(210, 0)
draw(config2, data2)

ctx.writesurface()

