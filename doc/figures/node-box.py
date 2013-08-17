import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 535
HEIGHT = 90


config1 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               box
    strokeWidth         0

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples2"
"""

config2 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               box
    strokeWidth         3
    strokeColor         bgColor

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples"
"""

config3 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               box
    strokeWidth         1.8
    strokeColor         baseColor
    horizSideColor      bgColor
    vertSideColor       bgColor

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples"
    fontColorAuto       no
    fontColor           baseColor
    fillColor           bgColor
"""

data1 = { 'unblazoned': [] }
data2 = { 'varmint': [] }
data3 = { 'wheedle': [] }


ctx.initsurface(1, 1, OUTFORMAT)
ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, OUTFILE, scale=0.8)
ctx.background(ctx.color(1))

ctx.translate(0, 10)
draw(config1, data1)

ctx.translate(200, 0)
draw(config2, data2)

ctx.translate(170, 0)
draw(config3, data3)

ctx.writesurface()

