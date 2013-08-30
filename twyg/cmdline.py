import os
import sys
import traceback
from optparse import OptionParser

from twyg import buildtree
from twyg.cairowrapper import context as ctx
from twyg.common import validate_margins, calculate_margins, loadjson
from twyg.config import loadconfig


def exit_error(msg):
    print >>sys.stderr, sys.argv[0] + ': ' + msg
    sys.exit(1)


def main():
    usage = 'Usage: %prog [OPTIONS] DATAFILE OUTFILE'
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--config',
                      dest='configfile', metavar='FILE',
                      help='path to the configuration file to use')

    parser.add_option('-o', '--colorscheme',
                      dest='colorscheme', metavar='NAME',
                      help='name of the colorscheme to use')

    parser.add_option('-d', '--dpi',
                      default='72.0', type='float',
                      help=('output resolution (PNG) or shadow rasterisation '
                            'resolution (PDF and SVG) [default: %default]'))

    parser.add_option('-m', '--margin',
                      default='10%,5%',
                      help=('margins in TOP,RIGHT,BOTTOM,LEFT or VERT,HORIZ '
                            'or MARGIN format; values are absolute (points) '
                            'or percentages [default: %default]'))

    # TODO
#    parser.add_option('-w', '--write-config',
#                      dest='writeconfig', metavar='FILE',
#                      help='output configuration file')

    parser.add_option('-v', '--verbose',
                      default=False, action='store_true',
                      help='display stack trace on error')

    parser.add_option('-s', '--scale',
                      default='1.0', type='float',
                      help=('scale factor (multiplier or percentage) '
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

    try:
        scale = options.dpi / 72.0 * options.scale     # 1 point = 1/72 inch

        # Temporary context for layout calculations (need an actual graphics
        # context to be able to work with fonts & text extents). Note that
        # 'None' is given for the output filename, so a failed run won't
        # overwrite an already existing file with an empty one. The actual
        # output file will be created later.
        ctx.initsurface(1, 1, options.outformat, None, scale)

        data = loadjson(datafile)
        config = loadconfig(options.configfile)

        tree = buildtree(data, config, options.colorscheme)

        width, height = tree.calclayout()

        # Margins can be given as percentages of the total graph size,
        # that's why we have to wait with the margin calculations until the
        # layout is complete
        padtop, padleft, padbottom, padright = calculate_margins(width, height,
                                                                 margins)
        width += padleft + padright
        height += padtop + padbottom

        # Create output file
        ctx.initsurface(width, height, options.outformat, outfile, scale)
        ctx.background(tree.background_color())

        # Center the graph
        ctx.translate(padleft, padtop)

        tree.draw()
        ctx.writesurface()

    except Exception, e:
        exit_error(traceback.format_exc() if options.verbose else str(e))

    return 0

