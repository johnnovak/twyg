Getting started
===============

Features
--------

* Generate pretty looking graphs using a procedural configuration language
* Trees are described in simple JSON format
* Powerful procedural configuration language to control all visual aspects of the
  resulting graphs
* 36 colorschemes and 15 configurations built-in
* Generate output from the command line using the Cairo backend
* Supports PDF, SVG and PNG output formats using the Cairo backend


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

This is the documentation for the Sphinx documentation builder.

