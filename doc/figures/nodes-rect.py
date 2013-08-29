import os, sys

from fig import *
from twyg.cairowrapper import context as ctx


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

tree1 = create_tree(config1, data1)
tree2 = create_tree(config2, data2)
tree3 = create_tree(config3, data3)

init_surface(500, 60, scale=0.8)

ctx.translate(7, 7)
tree1.draw()

ctx.translate(190, 0)
tree2.draw()

ctx.translate(155, 0)
tree3.draw()

ctx.writesurface()

