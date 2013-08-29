import os, sys

from fig import *
from twyg.cairowrapper import context as ctx


config1 = r"""
[layout]
    style                   layout

[node]
    style                   line
    fontName                $FONTNAME
    fontSize                $FONTSIZE
    textBaselineCorrection  $BASELINE_CORR
    strokeWidth             4

[connection]
    style                   curve

[color]
    style                   colorizer
    colorscheme             "mint-examples2"
"""


data1 = { 'daffadowndilly': [] }

init_surface(190, 50, scale=0.8)

ctx.translate(3, 3)
tree = create_tree(config1, data1)
tree.draw()

ctx.writesurface()

