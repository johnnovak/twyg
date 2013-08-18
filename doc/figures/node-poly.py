import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 390
HEIGHT = 110


config1 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               poly
    numSides            5
    strokeWidth         0
    rotation            18
    textPadX            15
    textPadY            15

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
    style               poly
    numSides            6
    strokeWidth         3
    textPadX            15
    textPadY            15

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
    style               poly
    numSides            8
    strokeWidth         6
    textPadX            15
    textPadY            15

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples3"
    fontColorAuto       no
    fontColor           #fff
    fillColor           baseColor.blend(#fff, .45)

"""

data1 = { 'lob': [] }
data2 = { 'boon': [] }
data3 = { 'mew': [] }


ctx.initsurface(1, 1, OUTFORMAT)
ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, OUTFILE, scale=0.8)
ctx.background(ctx.color(1))

ctx.translate(0, 15)
draw(config1, data1)

ctx.translate(136, -6)
draw(config2, data2)

ctx.translate(150, 3)
draw(config3, data3)

ctx.writesurface()

