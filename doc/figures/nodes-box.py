import os, sys

from fig import *
from twyg.cairowrapper import context as ctx


config1 = r"""
[layout]
    style                   layout

[node]
    style                   box
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             0
    textPadX                14
    textPadY                8

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
    style                   box
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             3
    strokeColor             bgColor
    textPadX                14
    textPadY                8

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
    style                   box
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             1.8
    strokeColor             baseColor
    horizSideColor          rgba(0, 0, 0, 0)
    vertSideColor           rgba(0, 0, 0, 0)
    textPadX                14
    textPadY                8

[connection]
    style                   curve

[color]
    style                   cycle
    colorscheme             "mint-examples"
    fontColorAuto           no
    fontColor               baseColor
    fillColor               rgba(0, 0, 0, 0)
"""


data1 = { 'unblazoned': [] }
data2 = { 'varmint': [] }
data3 = { 'wheedle': [] }

tree1 = create_tree(config1, data1)
tree2 = create_tree(config2, data2)
tree3 = create_tree(config3, data3)

init_surface(445, 65, scale=0.9)

ctx.translate(3, 3)
tree1.draw()

ctx.translate(172, 0)
tree2.draw()

ctx.translate(140, 0)
tree3.draw()

ctx.writesurface()

