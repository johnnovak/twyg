import os, sys

sys.path.append(os.path.join('../..'))

import twyg.common

from twyg import buildtree
from twyg.cairowrapper import context as ctx
from twyg.config import buildconfig, tokenize
from twyg.geom import Rectangle


twyg.common.TWYG_USER = os.path.join('.')
twyg.common.TWYG_HOME = os.path.join('../..')

IMG_DIR = 'images'
OUTFORMAT = 'png'
PAD_X = 3
PAD_Y = 3

TEMPLATE_VARS = {
    '$FONTNAME':       '"Open Sans"',
    '$FONTSIZE':       17,
    '$BASELINE_CORR':  -0.15
}

# Init drawing context
ctx.initsurface(1, 1, OUTFORMAT)


def write_tree(tree, w, h, suffix=None, scale=1.0):
    w += PAD_X * 2
    h += PAD_Y * 2
    if suffix:
        suffix = '-' + suffix
    init_surface(w, h, suffix=suffix, scale=scale)
    ctx.translate(PAD_X, PAD_Y)
    tree.draw()
    ctx.writesurface()


def init_surface(w, h, suffix='', scale=1.0):
    ctx.initsurface(w, h, OUTFORMAT, _imgname(OUTFORMAT, suffix), scale=scale)


def _imgname(ext, suffix=''):
    fname = os.path.splitext(sys.argv[0])[0] + suffix + '.' + ext
    return os.path.join(IMG_DIR, fname)


def write_all_trees(trees, scale=1.0):
    bbox = calc_bbox(trees)
    suffix = 'a'
    for t in trees:
        write_tree(t, bbox.w, bbox.h, suffix, scale)
        suffix = chr(ord(suffix) + 1)


def create_tree(config, data):
    config = _replace_template_vars(config)
    tokens = tokenize(config)
    config = buildconfig(tokens)
    tree = buildtree(data, config);
    tree.calclayout()
    return tree


def _replace_template_vars(config):
    for k, v in TEMPLATE_VARS.iteritems():
        config = config.replace(k, str(v))
    return config


def calc_bbox(trees):
    rect = Rectangle(0, 0, 0, 0)
    for t in trees:
        rect.expand(t.bbox)
    return rect

