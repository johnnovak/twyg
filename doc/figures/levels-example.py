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
  {default}
    style                   rect
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             3
    textPadX                20
    textPadY                10
    textAlign               center

  {leaf}
    @copy                   default
    levelNumChildrenMax     0
    style                   oval
    aspectRatio             2
    textPadX                3
    textPadY                0

  {root}
    @copy                   default
    levelDepthMax           0
    style                   poly
    numSides                8
    textPadX                8
    textPadY                8

[connection]
    style                   junction
    lineWidth               4
    cornerRadius            8
    cornerStyle             rounded
    cornerPad               0
    junctionStyle           none
    junctionRadius          14
    junctionXFactor         0.5

[color]
    style                   branch
    colorscheme             "mint-examples4"
    fontColor               color.white
    fontColorAuto           no
"""


data = { 'root': ['default1', {'default2': ['leaf1', 'leaf2']}, 'leaf3']}

scale = 0.75

t = create_tree(config, data)
write_tree(t, t.bbox.w, t.bbox.h, scale=scale)

