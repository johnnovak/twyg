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
    textPadX                22
    textPadY                8

[connection]
    style                   curve

[color]
    style                   cycle
    colorscheme             "mint-examples"
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
    textPadX                22
    textPadY                8

[connection]
    style                   curve

[color]
    style                   cycle
    colorscheme             "mint-examples2"
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
    textPadX                22
    textPadY                8

[connection]
    style                   curve

[color]
    style                   cycle
    colorscheme             "mint-examples3"
    fontColorAuto           no
    fontColor               #fff
"""


data1 = { 'penthouse': [] }
data2 = { 'roundured': [] }
data3 = { 'truncheon': [] }

scale = 0.8

trees = [
    create_tree(config1, data1),
    create_tree(config2, data2),
    create_tree(config3, data3)
]

write_all_trees(trees, scale)

