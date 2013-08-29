import os, sys

from fig import *


config = r"""
[layout]
    style                   layout
    horizontalBalance       0
    rootPadX                80
    nodePadX                80
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
    lineWidth               4
    cornerRadius            20
    cornerStyle             %s
    junctionStyle           disc
    junctionRadius          14
    junctionXFactor         0.5

[color]
    style                   colorizer
    colorscheme             "mint-examples%s"
"""


data = { 'A': ['B', 'C', 'D']}

scale = 0.75

trees = [
    create_tree(config % ('square', ''), data),
    create_tree(config % ('beveled', 2), data),
    create_tree(config % ('rounded', 3), data)
]

write_all_trees(trees, scale)

