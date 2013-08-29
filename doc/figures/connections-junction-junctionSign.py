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
    cornerStyle             rounded
    junctionStyle           disc
    junctionRadius          22
    junctionSign            %s
    junctionSignStrokeWidth 3.2
    junctionSignSize        12
    junctionXFactor         0.5
    junctionSignColor       #fff

[color]
    style                   colorizer
    colorscheme             "mint-examples%s"
"""


data = { 'A': ['B', 'C']}

scale = 0.75

trees = [
    create_tree(config % ('none', ''), data),
    create_tree(config % ('plus', 2),  data),
    create_tree(config % ('minus', 3), data)
]

write_all_trees(trees, scale)

