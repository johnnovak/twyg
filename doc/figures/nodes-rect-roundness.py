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
    roundness               0

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
    roundingStyle           screen
    roundness               0.5

[connection]
    style                   curve

[color]
    style                   colorizer
    colorscheme             "mint-examples3"
    fontColorAuto           no
    fontColor               #fff
"""

config3 = r"""
[layout]
    style                   layout

[node]
    style                   rect
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             3
    roundingStyle           screen
    roundness               1.0

[connection]
    style                   curve

[color]
    style                   colorizer
    colorscheme             "mint-examples3"
    fontColorAuto           no
    fontColor               #fff
"""


data1 = { 'r = 0.0': [] }
data2 = { 'r = 0.5': [] }
data3 = { 'r = 1.0': [] }

scale = 0.7

trees = [
    create_tree(config1, data1),
    create_tree(config2, data2),
    create_tree(config3, data3)
]

write_all_trees(trees, scale)

