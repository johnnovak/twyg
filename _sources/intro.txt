Getting started
===============

**twyg** lets you visualise arbitrary tree structures in a pretty way.  The
appearance of the tree (layout, color, node and connection shapes etc.) is
fully controlled via configuration files in a programmatic way. Comes with an
extensive set of default configurations and colorschemes. Requires Cairo (and
optionally PIL) for image generation when used from the command-line or can be
used as a NodeBox1 library.

.. image:: img/goals-boxes.png


Main Features
-------------

* Simple yet flexible configuration language to fully control all visual
  aspects of the tree
* Customisable layout and coloring algorithms
* Lots of fully customisable node and connections shapes
* Built-in configurations and colorschemes
* Tree structures are described in simple JSON files
* Can be used from the command-line with the Cairo backend or as a NodeBox1
  library
* PDF, SVG and PNG output formats
* Optionally requires PIL for drop-shadow support
* Python 2.5, 2.6 and 2.7 support
* Extensive documentation


Installation
------------

To install twyg for all users:

    $ sudo easy_install pip
    $ sudo pip install twyg


Quickstart
----------

Generate a PDF output of the tree `example1.json` using the built-in `nazca`
configuration::

    $ twyg.py --config nazca example1.json example.pdf

Generate a PNG file at 150 DPI from `example1.json` using the built-in `bubble`
configuration and use the `mint` colorscheme instead of the default one
specified in the config::

    $ twyg.py -c bubbles --colorscheme mint --dpi 150 example1.json example.png

Same as above, but leave 10% vertical and 20% horizontal margins::

    $ twyg.py -c bubbles -o mint --dpi 150 --margin=10%,20% example1.json example.png


Examples
--------

TODO

