import os, sys

from fig import *


config = r"""
[layout]
    style                   layout
    horizontalBalance       0
    rootPadX                80
    nodePadX                80
    nodePadY                10
    branchPadY              10
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
    cornerRadius            %s
    cornerStyle             beveled
    cornerPad               0
    junctionStyle           none
    junctionRadius          14
    junctionXFactor         0.5

[color]
    style                   colorizer
    colorscheme             "mint-examples%s"
"""


data = { 'A': ['B', {'C': ['X', 'Y']}, 'D']}

scale = 0.75

trees = [
    create_tree(config % (8, ''), data),
    create_tree(config % (1000, 3), data)
]

write_all_trees(trees, scale)

