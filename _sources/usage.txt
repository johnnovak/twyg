Usage
=====

Command line interface
----------------------

.. option:: -h, --help

    Show this help message and exit

.. option:: -c FILE, --config=FILE

    Config file

.. option:: -o FILE, --colorscheme=FILE

    Colorscheme file

.. option:: -d DPI, --dpi=DPI

    Output resolution (PNG) or shadow rasterisation resolution (PDF and
    SVG) [default: 72.0]

.. option:: -m MARGIN, --margin=MARGIN

    Margins in TOP,RIGHT,BOTTOM,LEFT or VERT,HORIZ or MARGIN format;
    values can be absolute points or percentages [default: 10%,5%]

.. option:: -v, --verbose
  
    Display extended error messages

.. option:: -s SCALE, --scale=SCALE

    Scale factor (absolute value or percentage) [default: 1.0]


NodeBox1
--------

Nodebox usage:

.. code-block:: python

    ximport('twyg')

    datafile = 'examples/data/data2.json'
    configfile = 'configs/synapse.twg'
    colorschemefile = 'colors/honey.twg'

    tree = twyg.buildtree(datafile, configfile, colorschemefile)

    width, height = tree.calclayout()

    size(width, height)
    background(tree.background_color())

    tree.draw()


See also *nodebox-usage.py*

