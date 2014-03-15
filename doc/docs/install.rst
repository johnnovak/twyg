Installation
============

Dependencies
------------

*twyg* is compatible with Python 2.5, 2.6 and 2.7.

When used as a standalone command line program, the `cairo
<http://cairographics.org/>`_ and `pango <http://www.pango.org/>`_ graphics
libraries and the `Pycairo <http://cairographics.org/pycairo/>`_ Python
bindings need to be installed for the graphics rendering.

Python 2.5 requires the `simplejson
<https://pypi.python.org/pypi/simplejson/>`_ Python module as well.

There are no prerequisites if it is used as a NodeBox1 library.


Command line usage
------------------

Installing the dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mac OS X
~~~~~~~~

.. code:: bash

    sudo port install py27-pip py27-cairo pango

Cygwin
~~~~~~

Install the ``pip``, ``cairo`` and ``pango`` packages with the Cygwin
installer tool.

Automatic installation
^^^^^^^^^^^^^^^^^^^^^^

*twyg* is registered at the Python Package Index (PyPI), so the simplest way
to install it is with the ``pip`` command:

.. code:: bash

    sudo pip install twyg

That's it.

.. note:: The installation package contains example data files and some useful
  scripts which won't be installed by using this method. You might want to
  download the package as well to get those files.

Manual installation
^^^^^^^^^^^^^^^^^^^

You can also download the installation package at PyPi and then install
manually:

.. code:: bash

    tar xvzf tywg-0.1.tar.gz
    cd tornado-0.1
    python setup.py build
    sudo python setup.py install

Then you will need to install the dependencies either via ``pip`` or your
operatings system's package manager.


NodeBox1 library (Mac OS X)
---------------------------

Download the installation package and just extract its contents into
``~/Library/Application\ Support/NodeBox``.
