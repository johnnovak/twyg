import os, sys

from fig import *
from twyg.cairowrapper import context as ctx


config1 = r"""
[layout]
    style                   layout

[node]
    style                   oval
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             0
    textPadX                14
    textPadY                14

[connection]
    style                   curve

[color]
    style                   colorizer
    colorscheme             "mint-examples"
"""

config2 = r"""
[layout]
    style                   layout

[node]
    style                   oval
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             3
    aspectRatio             .7
    textPadX                8
    textPadY                8

[connection]
    style                   curve

[color]
    style                   colorizer
    colorscheme             "mint-examples3"
"""

config3 = r"""
[layout]
    style                   layout

[node]
    style                   oval
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    aspectRatio             2
    strokeWidth             3
    textPadX                3
    textPadY                3

[connection]
    style                   curve

[color]
    style                   colorizer
    colorscheme             "mint-examples3"
    fontColorAuto           no
    fontColor               #fff
    fillColor               baseColor.blend(#fff, .45)

"""

data1 = { 'mar': [] }
data2 = { 'ere': [] }
data3 = { 'amiss': [] }

tree1 = create_tree(config1, data1)
tree2 = create_tree(config2, data2)
tree3 = create_tree(config3, data3)

init_surface(320, 83, scale=0.9)

ctx.translate(3, 3)
tree1.draw()

ctx.translate(120, 4)
tree2.draw()

ctx.translate(100, 9)
tree3.draw()

ctx.writesurface()

