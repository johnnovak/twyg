import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 375
HEIGHT = 85


config1 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               oval
    strokeWidth         0
    textPadX            10
    textPadY            10

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples"
"""

config2 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               oval
    strokeWidth         3
    aspectRatio         .7
    textPadX            8
    textPadY            8

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples3"
"""

config3 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               oval
    aspectRatio         2
    strokeWidth         3
    textPadX            3
    textPadY            3

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples3"
    fontColorAuto       no
    fontColor           #fff
    fillColor           baseColor.blend(#fff, .45)

"""

data1 = { 'mar': [] }
data2 = { 'ere': [] }
data3 = { 'amiss': [] }


ctx.initsurface(1, 1, OUTFORMAT)
ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, OUTFILE, scale=0.8)
ctx.background(ctx.color(1))

ctx.translate(1, 2)
draw(config1, data1)

ctx.translate(136, 0)
draw(config2, data2)

ctx.translate(117, 9)
draw(config3, data3)

ctx.writesurface()

