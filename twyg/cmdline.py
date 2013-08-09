import os
import sys
import traceback
from optparse import OptionParser

from twyg import buildtree
from twyg.cairowrapper import context as ctx
from twyg.common import validate_margins, calculate_margins


# Determine home directories
import twyg.common

if 'TWYG_HOME' in os.environ:
    twyg.common.TWYG_HOME = os.environ['TWYG_HOME']
else:
    twyg.common.TWYG_HOME = os.path.dirname(os.path.realpath(sys.argv[0]))

if 'TWYG_USER' in os.environ:
    twyg.common.TWYG_USER = os.environ['TWYG_USER']
else:
    twyg.common.TWYG_USER = '~/.twyg'


def exit_error(msg):
    print >>sys.stderr, sys.argv[0] + ': ' + msg
    sys.exit(1)


def main():
    usage = 'Usage: %prog [OPTIONS] DATAFILE OUTFILE'
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--config',
                      dest='configfile', metavar='FILE', help='config file')

    parser.add_option('-o', '--colorscheme',
                      dest='colorschemefile', metavar='FILE',
                      help='colorscheme file')

    parser.add_option('-d', '--dpi',
                      default='72.0', type='float',
                      help=('output resolution (PNG) or shadow rasterisation '
                            'resolution (PDF and SVG) [default: %default]'))

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
                      help=('scale factor (absolute value or percentage) '
                          '[default: %default]'))

    options, args = parser.parse_args()

    if len(args) == 0:
        parser.error('input and output files must be specified')
        return 2

    if len(args) == 1:
        parser.error('output file must be specified')
        return 2

    datafile = args[0]
    outfile = args[1]

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

    scale = options.dpi / 72.0 * options.scale     # 1 point = 1/72 inch

    # Temporary context for layout calculations (need an actual graphics
    # context to be able to work with fonts & text extents). Note that
    # 'None' is given for the output filename, so a failed run won't
    # overwrite an already existing file with an empty one. The actual
    # output file will be created later.
    ctx.initsurface(1, 1, options.outformat, None, scale)

    ###############
    ctx.initsurface(100, 150, options.outformat, outfile, scale)

    from twyg.common import createpath
    from twyg.geom import Vector2
    from twyg.geomutils import offset_poly

    elements = [
        Vector2(30, 30),
        Vector2(50, 40),
        Vector2(70, 20),
        Vector2(50, 50),
        Vector2(80, 60),
        Vector2(50, 80),
        Vector2(20, 70),
        Vector2(10, 40)
    ]
    elements = [
        Vector2(30, 35),
        Vector2(35, 30),
        Vector2(60, 30),
        Vector2(60, 60),
        Vector2(30, 60)
    ]
    elements = [
        Vector2(30, 30),
        Vector2(75, 35),
        Vector2(75, 60),
        Vector2(30, 90),
        Vector2(40, 50)
    ]

    p = createpath(ctx, elements, close=True)
    ctx.stroke(ctx.color(0))
    ctx.drawpath(p)

    exp = offset_poly(elements, 5)
    p = createpath(ctx, exp, close=True)
    ctx.stroke(ctx.color(1,0,0))
    ctx.drawpath(p)

    ctx.writesurface()
    return 0
    ###############

    try:
        tree = buildtree(datafile,
                         options.configfile,
                         options.colorschemefile)
    except Exception, e:
        exit_error(traceback.format_exc() if options.verbose else str(e))

    width, height = tree.calclayout()

    # Margins can be given as percentages of the total graph size,
    # that's why we have to wait with the margin calculations until the
    # layout is complete
    padtop, padleft, padbottom, padright = calculate_margins(width, height,
                                                             margins)
    width += padleft + padright
    height += padtop + padbottom

    # Center the graph
    tree.shiftnodes(padleft, padtop)

    # Create output file
    ctx.initsurface(width, height, options.outformat, outfile, scale)
    ctx.background(tree.background_color())
    tree.draw()
    ctx.writesurface()
    return 0

