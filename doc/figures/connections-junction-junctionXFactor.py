import os, sys

from fig import *


config = r"""
[layout]
    style                   layout
    horizontalBalance       0
    rootPadX                80
    nodePadX                80
    nodePadY                10
    radialMinNodes          1000
    sameWidthSiblings       no
    snapParentToChildren    yes

[node]
    style                   rect
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             3
    roundingStyle           arc
    cornerRadius            5
    textPadX                14
    textPadY                5

[connection]
    style                   junction
    lineWidth               3
    cornerRadius            20
    cornerStyle             rounded
    junctionStyle           square
    junctionRadius          12
    junctionFillColor       color.red
    junctionStrokeColor     color.red
    junctionXFactor         %s


[color]
    style                   cycle
    colorscheme             "mint-examples"
    connectionColor         #ea3
"""


data = { '1': [{'2': ['3', '4']}, '5', '6']}

scale = 0.75

trees = [
    create_tree(config % 0.0, data),
    create_tree(config % 0.5, data),
    create_tree(config % 1.0, data)
]

write_all_trees(trees, scale)

