import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 190
HEIGHT = 50


config1 = r"""
[layout]
    style               layout

[node]
    fontName            "Open Sans"
    style               line
    strokeWidth         4

[connection]
    style               curve

[color]
    style               colorizer
    colorscheme         "mint-examples2"
"""


data1 = { 'daffadowndilly': [] }


ctx.initsurface(1, 1, OUTFORMAT)
ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, OUTFILE, scale=0.8)
ctx.background(ctx.color(1))

ctx.translate(0, 0)
draw(config1, data1)

ctx.writesurface()

