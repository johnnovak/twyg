import os
import sys
import traceback
from optparse import OptionParser

from twyg import get_scale_factor, generate_output
from twyg.common import validate_margins


def exit_error(msg):
    print >>sys.stderr, sys.argv[0] + ': ' + msg
    sys.exit(1)


def main():
    usage = 'Usage: %prog [OPTIONS] DATAFILE OUTFILE'
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--config',
                      default='default',
                      dest='config', metavar='NAME',
                      help='configuration to use [default: %default]')

    parser.add_option('-o', '--colorscheme',
                      dest='colorscheme', metavar='NAME',
                      help='colorscheme to use')

    parser.add_option('-d', '--dpi',
                      default='72.0', type='float',
                      help=('output resolution (PNG) or shadow rasterisation '
                            'resolution (PDF, PS and SVG) [default: %default]'))

    parser.add_option('-m', '--margin',
                      default='10%,5%',
                      help=('margins in TOP,RIGHT,BOTTOM,LEFT or VERT,HORIZ '
                            'or MARGIN format, either as absolute units '
                            '(points) or percentages [default: %default]'))

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
    if ext in ('pdf', 'png', 'ps', 'svg'):
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
        scale = get_scale_factor(options.dpi, options.scale)

        generate_output(datafile, options.config, outfile, options.outformat,
                        colorscheme=options.colorscheme, scale=scale,
                        margins=margins)

    except Exception, e:
        exit_error(traceback.format_exc() if options.verbose else str(e))

    return 0

