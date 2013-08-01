#!/usr/bin/env python

# TODO remove debug
from twyg.geom import *
from twyg.geomutils import *
from time import time
################################

import os.path
import sys
import traceback
from optparse import OptionParser

from twyg import buildtree
from twyg.cairowrapper import context as ctx
from twyg.common import validate_margins, calculate_margins


def exit_error(msg):
    print >>sys.stderr, sys.argv[0] + ': ' + msg
    sys.exit(1)


def main():
    usage = 'Usage: %prog [OPTIONS] INFILE OUTFILE'
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--config',
                      dest='configfile', metavar='FILE', help='config file')

    parser.add_option('-d', '--dpi',
                      default='150.0', type='float',
                      help=('output resolution (PNG) or shadow rasterisation '
                            'resolution (PDF and SVG) [default: %default]'))

    parser.add_option('-i', '--input-format',
                      dest='informat', default='auto', metavar='FORMAT',
                      help=('input format: auto, json or text '
                            '[default: %default]'))

    parser.add_option('-m', '--margin',
                      default='10%,5%',
                      help=('margins in TOP,RIGHT,BOTTOM,LEFT or VERT,HORIZ '
                            'or MARGIN format; values can be absolute points '
                            'or percentages [default: %default]'))

    parser.add_option('-v', '--verbose',
                      default=False, action='store_true',
                      help='display extended error messages')

    parser.add_option('-s', '--scale',
                      default='1.0', type='float',
                      help='scale factor [default: %default]')

    options, args = parser.parse_args()

    if options.informat not in ('auto', 'json', 'text'):
        parser.error("input format '%s' is invalid" % options.input_format)
        return 2

    if len(args) == 0:
        parser.error('input and output files must be specified')
        return 2

    if len(args) == 1:
        parser.error('output file must be specified')
        return 2

    infile = args[0]
    outfile = args[1]

    if options.informat == 'auto':
        ext = os.path.splitext(infile)[1][1:].lower()
        options.informat = 'json' if ext == 'json' else 'text'

    ext = os.path.splitext(outfile)[1][1:].lower()
    if ext in ('pdf', 'png', 'svg'):
        options.outformat = ext
    else:
        parser.error('invalid output format: %s' % ext)
        return 2

    if options.dpi <= 0:
        parser.error('DPI value must be greater than 0')
        return 2

    if options.scale <= 0:
        parser.error('scale value must be greater than 0')
        return 2

    # Validate margin values
    margins = options.margin.split(',')
    try:
        validate_margins(margins)
    except ValueError, e:
        parser.error(e)
        return 2

    # Calculate output scale factor
    scale = options.dpi / 72.0 * options.scale     # 1 point = 1/72 inch

    # Set actual size later on
    ctx.initsurface(1, 1, options.outformat, outfile, scale)

    options.datafile = 'example-data/data4.json'
    options.configfile = 'configs/config8.twg'
    options.colorschemefile = 'colors/colors6b.twg'

    #options.datafile = 'example-data/data4.json'
    #options.configfile = 'configs/config3.twg'
    #options.colorschemefile = 'colors/colors11.twg'

    #options.datafile = 'example-data/data2-debug3.json'
    #options.configfile = 'configs/config8.twg'
    #options.colorschemefile = 'colors/colors12.twg'

    # with light grey bg
    #options.datafile = 'example-data/data2-debug.json'
    #options.configfile = 'configs/config8.twg'
    #options.colorschemefile = 'colors/colors6b.twg'

    # TODO error, empty page outputted
    #options.datafile = 'example-data/data1-big.json'

    # TODO
    #options.datafile = 'example-data/data1-big.json'
    #options.datafile = 'example-data/data1.json'
    #options.datafile = 'example-data/data1-debug4.json'

    #TODO
    #options.configfile = 'configs/config6.twg'

#    options.configfile = 'configs/config11.twg'
#    options.colorschemefile = 'colors/colors6.twg'

#    options.configfile = 'configs/config2.twg'
#    options.colorschemefile = 'colors/colors6.twg'

    try:
        tree = buildtree(options.datafile,
                         options.configfile,
                         options.colorschemefile)
    except Exception, e:
        exit_error(traceback.format_exc() if options.verbose else str(e))

    width, height = tree.calclayout()

    padtop, padleft, padbottom, padright = calculate_margins(width, height,
                                                             margins)
    width += padleft + padright
    height += padtop + padbottom

    tree.shiftnodes(padleft, padtop)

    ctx.initsurface(width, height, options.outformat, outfile, scale)
    ctx.background(tree.background_color())

# TODO remove debug
##############
#    ctx.stroke(0)
#
#    r = 10
#    p1 = Vector2(100, 100)
#    p15 = Vector2(200, 100)
#    p2 = Vector2(300, 100)
#    p3 = Vector2(300, 200)
#    p4 = Vector2(100, 200)
#
#    n = 1
#    t1 = time()
#    for i in range(n):
#        path = round_poly([p1, p2, p3, p4], r, close=True)
#    print 'round_poly: %s' % (time() - t1)
#
#    ctx.nofill()
#    ctx.stroke(.5)
#    ctx.strokewidth(1)
#
#    ctx.stroke(1,0,0)
#    ctx.strokewidth(1.5)
#
#    ctx.autoclosepath(False)
#    ctx.beginpath(path[0][0].x, path[0][0].y)
#    for p in path:
#        ctx.curveto(p[1].x, p[1].y, p[2].x, p[2].y, p[3].x, p[3].y)
#    ctx.endpath()
##############

    tree.draw()
    ctx.writesurface()

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)

