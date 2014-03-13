# twyg documentation

## Prerequisites

The documentation for **twyg** is written in reStructuredText / Sphinx.

The following tools need to be installed to generate the documentation:

* make
* Sphinx
* Sass
* twyg (e.g. installed with virtualenv in develop mode)
* Pycairo
* Python Imaging Library (PIL)


## Usage

The following master task will generate the full HTML documentation in
`_build/dirhtml`:

    make dirhtml_all

This consists of the following subtasks.

1. Generate the CSS from the Sass files:

    ```
    make update_css
    ```

2. Generate the figures:

    ```
    make figures
    ```

3. Generate the documentation from the reStructuredText sources and copy all
referenced static files *excluding* the example images:

    ```
    make dirhtml
    ```

4. Generate example images:

    ```
    make example
    ```

5. Copy example images to the output directory:

    ```
    make copy_examples
    ```

**NOTE:** Copying of example images is accomplished via a separate make
subtask, as opposed to letting Sphinx copy them as referenced static files.
This is for speed reasons — copying 24 megabytes of static data takes a bit
too long for my taste. This way you can just hit `make dirhtml` to regenerate
the documentation quickly.

***

To watch Sass file changes (generates the CSS automatically into the build dir
when a Sass change is detected):

    make watch_css

