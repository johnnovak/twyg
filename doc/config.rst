Configuration
=============


Sections
--------

style mandatory


*layout*

*node*

*connection*

*color*


Properties
----------


Variables
---------

*x*
    X position of the node

*y*
    Y position of the node

*fontSize*
    Font size used 

*width*
    Node width

*height*
    Node height

*bboxWidth*
    Bounding box width

*bboxHeight*
    Bounding box height

*textWidth*
    Text width

*textHeight*
    Text height

*maxTextWidth*
    Max text width

*bgColor*
    Background color

*baseColor*
    Base color

*fillColor*
    Fill color

*strokeColor*
    Stroke color

*fontColor*
    Font color

*lineHeight*
    Line height


Functions
---------

Mathematical functions
^^^^^^^^^^^^^^^^^^^^^^

.. function:: abs(x)

    Return the absolute value of *x*.


.. function:: ceil(x)

    Return the smallest integer value greater than or equal to *x*.


.. function:: floor(x)

    Return the larger integer value less than or equal to *x*.


.. function:: log(x)

    Return the natural (base-e) logarithm of *x*.


.. function:: log10(x)

    Return the base-10 logarithm of *x*.


.. function:: max(x, y)

    Return the largest of two values.


.. function:: min(x, y)

    Return the smallest of two values.


.. function:: pow(x, y)

    Return *x* to the power of *y*.


.. function:: round(x)

    Round *x* to the nearest integer value.


.. function:: sqrt(x)

    Return the square root of *x*.



Colors
------

Colors can be specified in either hexadecimal or functional CSS3 notation.
Below are some examples of valid CSS3 color definitions::

    #ff8
    #00427a
    rgb(100, 100, 255)
    rgb(11%, 20%, 42%)
    rgba(255, 0, 79, 0.4)
    rgba(11%, 100%, 0%, 0.1)
    hsl(130, 30%, 80%)
    hsla(99, 12%, 74%, 0.33)

Colors can also be specified using `SVG 1.0 color keyword names
<http://www.w3.org/TR/css3-color/#svg-color>`_ in *color.<colorname>* format::

    color.yellow
    color.azure
    color.darkseagreen

For a comprehensive description of CSS3 color notation refer to `Section 4
<http://www.w3.org/TR/css3-color/>`_ of the `CSS Color Module Level 3
<http://www.w3.org/TR/css3-color/#colorunits>`_ specification.


Color functions
^^^^^^^^^^^^^^^

There are a number of functions that can be used to manipulate colors. These
functions can be invoked using the *<color>.<function>* notation::

    #ff8.lighten(0.5)
    color.blue.darken(0.2)
    rgb(11%, 20%, 42%).blend(#fff, 0.5)

The following color manipulation functions are available. The value of *factor*
should be between *0.0-1.0* in all cases.

.. function:: darken(factor)

    Darkens the color by a given factor. ::

        color.red.darken(0.5)
        #48a70f.darken(0.3)


.. function:: lighten(factor)

    Darkens the color by a given factor.  ::

        color.fuchsia.lighten(0.3)
        hsla(88, 30%, 68%, 0.7).lighten(.7)


.. function:: blend(destcol, factor)
     
    Blends the color with *destcolor* by a given factor. ::

        #118833.blend(#fff, 0.8)
        #777.blend(color.red, 0.6)
        baseColor.blend(bgColor, 0.2)

.. tip:: Blending a color with white or black results in a different, less
    saturated shade than using the *lighten* and *darken* functions to
    manipulate brightness. This might be preferable in some situations. The
    following table illustrates the difference between the two methods:

    .. image:: figures/images/color-blending.png
       :align: center



Directives
----------

*@copy*
    Copy level definition.

*@include*
    Include another config file.

    Search path:

    * Current directory (the directory the script was started in)
    * $TWYG_USER/configs
    * $TWYG_HOME/configs


Levels
------

.. property:: levelDepthMin

    .. propparams:: Number 0
        :values: >0

    Minimum depth the node must have for the level definition to apply to it.


.. property:: levelDepthMax

    .. propparams:: Number 999999999
        :values: >0

    Maximum depth the node can have for the level definition to apply to it.


.. property:: levelNumChildrenMin 

   .. propparams:: Number 0
       :values: >0

   Minimum number of child nodes the node must have for the level definition to
   apply to it.


.. property:: levelNumChildrenMax 

   .. propparams:: Number 999999999
       :values: >0

   Maximum number of child nodes the node can have for the level
   definition to apply to it.


.. property:: levelOrientation 

   .. propparams:: Enum any
       :values: top | right | bottom | left | any

   TODO


Some level selector examples:

    * Select root node only::

          {root}
          levelDepthMax 0


    * Select all leaf nodes::

          {leaf}
          levelNumChildrenMax 0


    * Select leaf nodes at depth 2 at least::

          {leaf}
          levelDepthMin 2
          levelNumChildrenMax 0


A more complex example using @copy in conjunction with levels::

    [node]
      {normal}
        style                   rect
        strokeWidth             3
        roundness               1.0
        roundingStyle           arc
        cornerRadius            40

      {root}
        @copy normal
        levelDepthMax           0

        cornerRadius            80

      {leaf}
        levelNumChildrenMax     0
        style                   line
        strokeWidth             3




