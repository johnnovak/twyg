#!/usr/bin/env python

import os
import subprocess
import sys


TWYG_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

TWYG_CMD = os.path.join(TWYG_HOME, 'twyg.py')


examples = [
   { # 0
    'config': 'configs/config1.twg',
    'color':  'colors/colors4.twg',
    'data':   'examples/data/data7.json'

}, { # 1
    'config': 'configs/config2.twg',
    'color':  'colors/colors6.twg',
    'data':   'examples/data/data1.json'

}, { # 2
    'config': 'configs/config3.twg',
    'color':  'colors/colors1.twg',
    'data':   'examples/data/data4.json'

}, { # 3
    'config': 'configs/config4.twg',
    'color':  'colors/colors9.twg',
    'data':   'examples/data/data5.json'

}, { # 5
    'config': 'configs/config6.twg',
    'color':  'colors/colors10.twg',
    'data':   'examples/data/data4.json'

}, { # 6
    'config': 'configs/config7.twg',
    'color':  'colors/colors4.twg',
    'data':   'examples/data/data3.json'

}, { # 7
    'config': 'configs/config8.twg',
    'color':  'colors/colors6b.twg',
    'data':   'examples/data/data5.json'

}, { # 0
    'config': 'configs/config9.twg',
    'color':  'colors/colors6.twg',
    'data':   'examples/data/data5.json'

}, { # 0
    'config': 'configs/config10.twg',
    'color':  'colors/colors6.twg',
    'data':   'examples/data/data5.json'

}, { # 0
    'config': 'configs/config11.twg',
    'color':  'colors/colors6.twg',
    'data':   'examples/data/data5.json'





}, { # 0
    'config': 'configs/config3.twg',
    'color':  'colors/colors2.twg',
    'data':   'examples/data/data3.json'

}, { # 0
    'config': 'configs/config1.twg',
    'color':  'colors/colors4.twg',
    'data':   'examples/data/data5.json'

}, { # 1
    'config': 'configs/config2.twg',
    'color':  'colors/colors3.twg',
    'data':   'examples/data/data2-debug3.json'

}, { # 2
    'config': 'configs/config8.twg',
    'color':  'colors/colors12.twg',
    'data':   'examples/data/data4.json'

}, { # 3
    'config': 'configs/config8.twg',
    'color':  'colors/colors6b.twg',
    'data':   'examples/data/data5.json'

}, { # 3
    'config': 'configs/config11.twg',
    'color':  'colors/colors6.twg',
    'data':   'examples/data/data4.json'

}, { # 4
    'config': 'configs/config2.twg',
    'color':  'colors/colors6.twg',
    'data':   'examples/data/data5.json'

}, { # 4
    'config': 'configs/config12.twg',
    'color':  'colors/colors6.twg',
    'data':   'examples/data/cocoa.json'
}]


def generate_example(n, outfile, format):
    ex = examples[n]
    outfile = outfile + '.' + format
    args = [
        TWYG_CMD,
        '-c', os.path.join(TWYG_HOME, ex['config']),
        '-o', os.path.join(TWYG_HOME, ex['color']),
        os.path.join(TWYG_HOME, ex['data']),
        outfile
    ]
    print "Executing command:", ' '.join(args)
    po = subprocess.Popen(args)
    ret = po.wait()


def generate_all_examples(format):
    for n in range(len(examples)):
        generate_example(n, 'example%s' % n, format)


if __name__ == '__main__':
    generate_all_examples('pdf')
#    generate_all_examples('png')
#    generate_all_examples('svg')

