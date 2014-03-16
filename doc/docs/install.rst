Installation
============

Prerequisites
-------------

*twyg* is compatible with Python 2.5, 2.6 and 2.7.

When used as a standalone command line program, the `cairo
<http://cairographics.org/>`_ and `pango <http://www.pango.org/>`_ graphics
libraries and the `Pycairo <http://cairographics.org/pycairo/>`_ Python
bindings need to be installed for graphics rendering.

Python 2.5 requires the `simplejson
<https://pypi.python.org/pypi/simplejson/>`_ Python module as well.

There are no prerequisites if it is used as a NodeBox1 library (see :ref:`nodebox1-setup`).


Download
--------

If you wish to install *twyg* automatically with ``pip``, you don't need to
download anything. Just proceed to the :ref:`install-deps` section.

If you want to do a manual install, you can download the `latest distribution
package <#>`_ from the `Python Package Index (PyPi)
<https://pypi.python.org/pypi>`_. Alternatively, you can download the latest development version as a
`ZIP file <https://github.com/johnnovak/twyg/archive/master.zip>`_ from the
project's `GitHub page <https://github.com/johnnovak/twyg>`_,
or clone the repository if you are familiar with ``git``.

You can also download the `offline documentation <#>`_ here.

.. note:: The installation package contains example data files and some useful
    scripts that won't be installed when using the automatic installation
    method with ``pip``. You might want to download the package as well to get
    those files.


.. _install-deps:

Install dependencies
--------------------

Below are platform specific instructions on installing the dependencies
required by **twyg**.

Mac OS X
^^^^^^^^

1. Install MacPorts
~~~~~~~~~~~~~~~~~~~

The easiest way to install the dependent libraries on Mac OS X is to use `MacPorts <http://www.macports.org/>`_. If you already have MacPorts
on your system, just proceed with the following step. Otherwise, follow 
`these instructions <http://www.macports.org/install.php>`_ to install
MacPorts first.

2. Install dependencies
~~~~~~~~~~~~~~~~~~~~~~~

The following command will install *cairo* and the *Pycairo* Python bindings.
It will install *Python 2.7* as well, if it's not already installed (that will
take a while):

.. code-block:: bash

    sudo port install py27-cairo

If you wish to do an automatic install, you'll need to install *pip* as
well:

.. code-block:: bash

    sudo port install py27-pip

After the above commands have successfully completed, make Python 2.7 the
default installation:

.. code-block:: bash

    sudo port select --set python python27

.. note:: If you wish to use an earlier Python version, change all occurences
  of ``27`` to ``26`` or ``25`` in the above commands.


Linux
^^^^^

Install **Pycairo** with your distribution's package manager.

Cygwin
^^^^^^

Install the **pip**, **cairo** and **pango** packages with the Cygwin installer
tool.

Windows
^^^^^^^

TODO

Install twyg
------------

*1. Automatic method*

To install **twyg** automatically with **pip**, issue the following command:

.. code-block:: bash

    pip install twyg


*2. Manual method*

Alternatively, you can do a manual install if you have downloaded the
distribution package:

.. code-block:: bash

    tar xzf twyg-0.1.tgz
    cd twyg-0.1
    python setup.py build
    sudo python setup.py install


.. _nodebox1-setup:

NodeBox1 setup
--------------

Download the `distribution package <#>`_ and extract its contents somewhere.
Copy the ``twyg`` subfolder from the folder you extracted the package to into
``~/Library/Application\ Support/NodeBox`` .

