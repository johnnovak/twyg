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
    lineWidth               4
    cornerRadius            20
    cornerStyle             rounded
    junctionStyle           %s
    junctionRadius          %s
    junctionXFactor         0.5

[color]
    style                   cycle
    colorscheme             "mint-examples%s"
"""


data = { 'A': ['B', 'C']}

scale = 0.75

trees = [
    create_tree(config % ('none', 14, ''), data),
    create_tree(config % ('square', 14, 2), data),
    create_tree(config % ('disc', 14, 3), data),
    create_tree(config % ('diamond', 20, 3), data)
]

write_all_trees(trees, scale)

