Prerequisites
-------------

The documentation for *twyg* is written in reStructuredText / Sphinx.

The following tools are needed to generate the documentation:

* make
* Sphinx
* Sass
* twyg (e.g. installed with virtualenv in develop mode)
* Pycairo and PIL for image generation

Usage
-----

These commands will generate the full HTML documenation in `_build/html`:

    make figures
    make html

To regenerate the CSS from the Sass files only:

    make update_css

To watch Sass files changes (generates CSS automatically when a change is
detected):

    make watch_css
