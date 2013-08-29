import os, sys

from fig import *


config1 = r"""
[layout]
    style                   layout

[node]
    style                   rect
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             3
    roundingStyle           screen

[connection]
    style                   curve

[color]
    style                   colorizer
    colorscheme             "mint-examples3"
    fontColorAuto           no
    fontColor               #fff
"""

config2 = r"""
[layout]
    style                   layout

[node]
    style                   rect
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             3
    roundingStyle           arc
    cornerRadius            25

[connection]
    style                   curve

[color]
    style                   colorizer
    colorscheme             "mint-examples3"
    fontColorAuto           no
    fontColor               #fff
"""


data1 = { 'screen': [] }
data2 = { 'arc': [] }

scale = 0.7

trees = [
    create_tree(config1, data1),
    create_tree(config2, data2)
]

write_all_trees(trees, scale)

