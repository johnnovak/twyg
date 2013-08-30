import os, sys

from fig import *
from twyg.cairowrapper import context as ctx


config1 = r"""
[layout]
    style                   layout

[node]
    style                   poly
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    numSides                5
    strokeWidth             0
    rotation                18
    textPadX                15
    textPadY                15

[connection]
    style                   curve

[color]
    style                   cycle
    colorscheme             "mint-examples2"
"""

config2 = r"""
[layout]
    style                   layout

[node]
    style                   poly
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    numSides                6
    strokeWidth             3
    textPadX                15
    textPadY                15

[connection]
    style                   curve

[color]
    style                   cycle
    colorscheme             "mint-examples"
"""

config3 = r"""
[layout]
    style                   layout

[node]
    style                   poly
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    numSides                8
    strokeWidth             6
    textPadX                15
    textPadY                15

[connection]
    style                   curve

[color]
    style                   cycle
    colorscheme             "mint-examples3"
    fontColorAuto           no
    fontColor               #fff
    fillColor               baseColor.blend(#fff, .45)

"""

data1 = { 'lob': [] }
data2 = { 'boon': [] }
data3 = { 'mew': [] }

tree1 = create_tree(config1, data1)
tree2 = create_tree(config2, data2)
tree3 = create_tree(config3, data3)

init_surface(340, 100, scale=0.9)

ctx.translate(3, 15)
tree1.draw()

ctx.translate(120, -6)
tree2.draw()

ctx.translate(130, 3)
tree3.draw()

ctx.writesurface()

