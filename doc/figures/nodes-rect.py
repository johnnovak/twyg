import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 500
HEIGHT = 60


config1 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               rect
    strokeWidth         3
    roundness           0

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples"
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
    roundness           1.0

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples2"
"""

config3 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               rect
    strokeWidth         3
    roundingStyle       arc
    cornerRadius        45

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples3"
    fillColor           baseColor.blend(#fff, .8)
"""


data1 = { 'mischance': [] }
data2 = { 'succour': [] }
data3 = { 'trapessing': [] }


ctx.initsurface(1, 1, OUTFORMAT)
ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, OUTFILE, scale=0.8)
ctx.background(ctx.color(1))

ctx.translate(7, 7)
draw(config1, data1)

ctx.translate(190, 0)
draw(config2, data2)

ctx.translate(155, 0)
draw(config3, data3)

ctx.writesurface()

