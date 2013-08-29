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

[connection]
    style                   curve

[color]
    style                   colorizer
    colorscheme             "mint-examples3"
    fontColorAuto           no
    fontColor               #fff
"""


scale = 0.7

data1 = { 'stuff': [] }
data2 = { 'stuff': [] }
data3 = { 'stuff': [] }

trees = [
    create_tree(config % 5, data1),
    create_tree(config % 10, data2),
    create_tree(config % 1000, data3)
]

write_all_trees(trees, scale)

