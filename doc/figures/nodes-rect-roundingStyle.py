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
    textPadX                22
    textPadY                8

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
    textPadX                22
    textPadY                8

[connection]
    style                   curve

[color]
    style                   colorizer
    colorscheme             "mint-examples"
    fontColorAuto           no
    fontColor               #fff
"""


data1 = { 'toothsome': [] }
data2 = { 'flittermice': [] }

scale = 0.8

trees = [
    create_tree(config1, data1),
    create_tree(config2, data2)
]

write_all_trees(trees, scale)

