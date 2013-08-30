import os, sys

from fig import *
from twyg.cairowrapper import context as ctx


config1 = r"""
[layout]
    style                   layout
    horizontalBalance       0
    rootPadX                110
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
    roundness               1.0
    roundingStyle           arc
    cornerRadius            7
    textPadX                15
    textPadY                5

[connection]
    style                   junction
    lineWidth               4
    cornerRadius            20
    cornerStyle             rounded
    junctionStyle           disc
    junctionRadius          20
    junctionXFactor         0.55
    junctionSign            plus
    junctionSignStrokeWidth 3
    junctionSignColor       #fff


[color]
    style                   cycle
    colorscheme             "mint-examples"
"""

config2 = r"""
[layout]
    style                   layout
    horizontalBalance       0
    rootPadX                110
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
    roundness               0
    textPadX                15
    textPadY                5

[connection]
    style                   junction
    lineWidth               3
    cornerRadius            20
    cornerStyle             beveled
    junctionStyle           square
    junctionRadius          10
    junctionXFactor         0.55


[color]
    style                   cycle
    colorscheme             "mint-examples2"
"""

config3 = r"""
[layout]
    style                   layout
    horizontalBalance       0
    rootPadX                110
    nodePadY                10
    radialMinNodes          1000
    sameWidthSiblings       no
    snapParentToChildren    yes

[node]
  {normal}
    style                   rect
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             3
    roundness               0
    cornerRadius            7
    textPadX                15
    textPadY                5

[connection]
    style                   junction
    lineWidth               5
    cornerRadius            20
    cornerStyle             square
    junctionStyle           none
    junctionRadius          10
    junctionXFactor         0.55

[color]
    style                   cycle
    colorscheme             "mint-examples3"
"""

data1 = { 'barrel': ['flank', 'stem', 'grot']}
data2 = { 'barrel': ['flank', 'stem', 'grot']}
data3 = { '7381': ['331', '102', '445', '983']}

init_surface(865, 165, scale=0.75)

tree1 = create_tree(config1, data1)
tree2 = create_tree(config2, data2)
tree3 = create_tree(config3, data3)

ctx.translate(3, 3)
tree1.draw()

ctx.translate(310, 0)
tree2.draw()

ctx.translate(310, 0)
tree3.draw()

ctx.writesurface()
