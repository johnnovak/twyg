import os, sys

from fig import draw, imgname
from twyg.cairowrapper import context as ctx


OUTFORMAT = 'png'
OUTFILE = imgname(OUTFORMAT)
WIDTH = 900
HEIGHT = 170


config1 = r"""
[layout]
    style                   layout
    horizontalBalance       0
    rootPadX                110
    radialMinNodes          1000
    sameWidthSiblings       no
    snapParentToChildren    yes

[node]
    style                   rect
    fontName                "Open Sans"
    fontSize                17
    strokeWidth             3
    roundness               1.0
    roundingStyle           arc
    cornerRadius            7
    textPadX                15
    textPadY                5

[connection]
    style                   junction 
    lineWidth               4
    cornerRadius            20
    cornerStyle             rounded
    junctionStyle           disc
    junctionRadius          20
    junctionXFactor         0.55
    junctionSign            plus
    junctionSignStrokeWidth 3
    junctionSignColor       #fff


[color]
    style               colorizer
    colorscheme         "mint-examples"
"""

config2 = r"""
[layout]
    style                   layout
    horizontalBalance       0
    rootPadX                110
    radialMinNodes          1000
    sameWidthSiblings       no
    snapParentToChildren    yes

[node]
    style                   rect
    fontName                "Open Sans"
    fontSize                17
    strokeWidth             3
    roundness               0
    textPadX                15
    textPadY                5

[connection]
    style                   junction 
    lineWidth               3
    cornerRadius            20
    cornerStyle             beveled
    junctionStyle           square
    junctionRadius          10
    junctionXFactor         0.55


[color]
    style               colorizer
    colorscheme         "mint-examples2"
"""

config3 = r"""
[layout]
    style                   layout
    horizontalBalance       0
    rootPadX                110
    radialMinNodes          1000
    sameWidthSiblings       no
    snapParentToChildren    yes

[node]
  {normal}
    style                   rect
    fontName                "Open Sans"
    fontSize                17
    strokeWidth             3
    roundness               0
    cornerRadius            7
    textPadX                15
    textPadY                5

[connection]
    style                   junction 
    lineWidth               5
    cornerRadius            20
    cornerStyle             square
    junctionStyle           none
    junctionRadius          10
    junctionXFactor         0.55

[color]
    style               colorizer
    colorscheme         "mint-examples3"
"""

data1 = { 'barrel': ['flank', 'stem', 'grot']}
data2 = { 'barrel': ['flank', 'stem', 'grot']}
data3 = { '7381': ['331', '102', '445', '983']}

ctx.initsurface(1, 1, OUTFORMAT)
ctx.initsurface(WIDTH, HEIGHT, OUTFORMAT, OUTFILE, scale=0.75)
ctx.background(ctx.color(1))

ctx.translate(3, 3)
draw(config1, data1)

ctx.translate(320, 0)
draw(config2, data2)

ctx.translate(320, 0)
draw(config3, data3)

ctx.writesurface()

