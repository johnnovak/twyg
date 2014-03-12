#!/usr/bin/env python

import os

from twyg import get_scale_factor, generate_output


DATA_PATH = '../../example-data'
OUT_PATH = '.'

DA = 'google-analytics'
DC = 'cocoa'
DG = 'goals'
DM = 'metrics'
DN = 'animals'
DS = 'six-thinking-hats'
DU = 'guitars'
DW = 'wind-instruments'
DY = 'synthesis'

configs = [
    {'boxes':     [{ 'data': DC, 'colors': 'kelp' },
                   { 'data': DG, 'colors': '' },
                   { 'data': DM, 'colors': 'moon' }]
    },
    {'bubbles':   [{ 'data': DA, 'colors': 'inca' },
                   { 'data': DM, 'colors': '' },
                   { 'data': DS, 'colors': 'neo' }]
    },
    {'flowchart': [{ 'data': DA, 'colors': 'inca' },
                   { 'data': DM, 'colors': '' },
                   { 'data': DW, 'colors': 'jelly' }]
    },
    {'hive':      [{ 'data': DG, 'colors': 'jelly' },
                   { 'data': DS, 'colors': '' },
                   { 'data': DY, 'colors': 'mango' }]
    },
    {'ios':       [{ 'data': DM, 'colors': 'milkshake' },
                   { 'data': DS, 'colors': 'honey' },
                   { 'data': DY, 'colors': '' }]
    },
    {'junction1': [{ 'data': DN, 'colors': 'forest' },
                   { 'data': DM, 'colors': 'clay' },
                   { 'data': DW, 'colors': '' }]
    },
    {'junction2': [{ 'data': DN, 'colors': 'mango' },
                   { 'data': DU, 'colors': '' },
                   { 'data': DW, 'colors': 'salmon' }]
    },
    {'lines':     [{ 'data': DN, 'colors': '' },
                   { 'data': DA, 'colors': 'merlot' },
                   { 'data': DM, 'colors': 'inca' }]
    },
    {'modern':    [{ 'data': DN, 'colors': '' },
                   { 'data': DM, 'colors': 'forest' },
                   { 'data': DY, 'colors': 'cobalt' }]
    },
    {'nazca':     [{ 'data': DC, 'colors': 'cmyk' },
                   { 'data': DM, 'colors': 'aqua' },
                   { 'data': DY, 'colors': '' }]
    },
    {'rounded':   [{ 'data': DG, 'colors': '' },
                   { 'data': DA, 'colors': 'orbit' },
                   { 'data': DM, 'colors': 'grape' }]
    },
    {'square':    [{ 'data': DN, 'colors': 'quartz' },
                   { 'data': DC, 'colors': 'crayons' },
                   { 'data': DU, 'colors': '' }]
    },
    {'synapse':   [{ 'data': DC, 'colors': 'kelp' },
                   { 'data': DA, 'colors': 'mint' },
                   { 'data': DM, 'colors': '' }]
    },
    {'tron':      [{ 'data': DC, 'colors': '' },
                   { 'data': DM, 'colors': 'mellow' },
                   { 'data': DY, 'colors': 'colors21' }]
    }
]


def generate_examples(outformat, dpi):
    for c in configs:
        config_fname = c.keys()[0]
        params = c.values()[0]

        for p in params:
            data_fname = os.path.join(DATA_PATH, p['data'] + '.json')
            colorscheme = p['colors']

            out_fname = [config_fname]
            if colorscheme:
                out_fname.append(colorscheme)
            out_fname.append(os.path.basename(os.path.splitext(data_fname)[0]))

            out_fname = os.path.join(OUT_PATH, outformat,
                                     '-'.join(out_fname) + '.' + outformat)

            print "Generating '%s'..." % out_fname,
            scale = get_scale_factor(dpi, 1.0);
            generate_output(data_fname, config_fname, out_fname, outformat,
                            colorscheme=colorscheme, scale=scale)
            print 'OK'


generate_examples('pdf', 72)
generate_examples('svg', 72)
generate_examples('png', 150)

