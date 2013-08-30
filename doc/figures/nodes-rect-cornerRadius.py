import os, sys

from fig import *


config = r"""
[layout]
    style                   layout

[node]
    style                   rect
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             3
    roundingStyle           arc
    cornerRadius            %s
    textPadX                25
    textPadY                8

[connection]
    style                   curve

[color]
    style                   colorizer
    colorscheme             "mint-examples%s"
    fontColorAuto           no
    fontColor               #fff
"""


scale = 0.8

data1 = { 'constellate': [] }
data2 = { 'mattock': [] }
data3 = { 'umbraged': [] }

trees = [
    create_tree(config % (5, 3), data1),
    create_tree(config % (10, ''), data2),
    create_tree(config % (1000, 2), data3)
]

write_all_trees(trees, scale)

