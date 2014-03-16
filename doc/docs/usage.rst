Usage
=====

Command line interface
----------------------

**twyg** understands the following command line options:

.. option:: -h, --help

    Print a short summary of the available command line options and exit.

.. option:: -c NAME, --config=FILE

    Name of the configuration to use. The ``default`` configuration is used if
    not specified.

.. option:: -o NAME, --colorscheme=NAME

    Name of the colorscheme to use. Use this option to override the
    colorscheme specified in the configuration. The ``default`` configuration
    is used if not specified.

.. option:: -d DPI, --dpi=DPI

    For PNG output, this option sets the output resolution (DPI) of the raster
    image.

    For vector output formats (PDF, PostScript and SVG), the value controls
    the rasterisation resolution of the drop shadow images. Use the
    ``--scale`` option to control the size of the resulting image instead.

    The default DPI value is ``72.0``

.. option:: -m MARGIN, --margin=MARGIN

    Margins in TOP,RIGHT,BOTTOM,LEFT or VERT,HORIZ or MARGIN format.
    Margin values can be absolute points or percentages.

    The default margin value is ``10%,5%``

.. option:: -v, --verbose
  
    Display extended error messages. This could be useful when you would like
    to report a defect.

.. option:: -s SCALE, --scale=SCALE

    Scale factor (absolute value or percentage). This is useful to scale
    the size image when using vector output formats.

    The default scale factor is ``1.0``


NodeBox1
--------

Using *twyg* as a NodeBox1 library is pretty simple:

.. code-block:: python

    ximport('twyg')

    datafile = '/path/to/example-data/synthesis.json'
    config = 'hive'
    colorscheme = 'orbit'
    margins = ['10%', '5%']

    twyg.generate_output_nodebox(datafile, config, colorscheme=colorscheme, margins=margins)


That's it.
