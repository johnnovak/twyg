#!/usr/bin/env python

import os.path
import sys
import traceback
from optparse import OptionParser

from twyg import buildtree
from twyg.cairowrapper import context as ctx
from twyg.common import validate_margins, calculate_margins
from twyg.css3colors import color_to_rgba


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

    parser.add_option('-b', '--background-color',
                      dest='bgcolor', metavar='COLOR',
                      help=('override background color; must be '
                            'specified in CSS3 format'))

    parser.add_option('-d', '--dpi',
                      default='150.0', type='float',
                      help=('output resolution (PNG) or shadow rasterisation '
                            'resolution (PDF and SVG) [default: %default]'))

    parser.add_option('-i', '--input-format',
                      dest='informat', default='auto', metavar='FORMAT',
                      help=('input format; auto, json or text '
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
                      help='scale factor as multiplier or percentage [default: %default]')

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

    datafile = args[0]
    outfile = args[1]

    if options.informat == 'auto':
        ext = os.path.splitext(datafile)[1][1:].lower()
        options.informat = 'json' if ext == 'json' else 'text'

    # TODO implement text input format parsing

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

    # TODO interpret scale factor either as a multiplier or a percentage
    # Calculate output scale factor
    scale = options.dpi / 72.0 * options.scale     # 1 point = 1/72 inch

    # Set actual size later on
    ctx.initsurface(1, 1, options.outformat, outfile, scale)


    # SAMPLES

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

    ctx.initsurface(width, height, options.outformat, outfile, scale)

    # Override background color is specified on the command line
    if options.bgcolor:
        # TODO refactor color(*color_to_rgba) to parsecolor in common
        bgcolor = ctx.color(*color_to_rgba(options.bgcolor))
    else:
        bgcolor = tree.background_color()

    ctx.background(bgcolor)

    tree.draw()
    ctx.writesurface()

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)

