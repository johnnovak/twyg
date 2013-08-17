import os, sys

sys.path.append(os.path.join('../..'))

import twyg.common

from twyg import buildtree
from twyg.cairowrapper import context as ctx
from twyg.config import buildconfig, tokenize


twyg.common.TWYG_HOME = os.path.join('../..')


def draw(config, data):
    tokens = tokenize(config)
    config = buildconfig(tokens)

    tree = buildtree(data, config);
    tree.calclayout()
    tree.draw()


def imgname(ext):
    return os.path.splitext(sys.argv[0])[0] + '.' + ext

