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

.. function:: abs(n)

.. function:: ceil(n)

.. function:: floor(n)

.. function:: log(n)

.. function:: log10(n)

.. function:: max(a, b)

.. function:: min(a, b)

.. function:: pow(n, p)

.. function:: round(n)

.. function:: sqrt(n)


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

For a comprehensive description of CSS3 color format refer to `Section 4
<http://www.w3.org/TR/css3-color/>`_ of the `CSS Color Module Level 3
<http://www.w3.org/TR/css3-color/#colorunits>`_ specification.

Colors can also be specified using `SVG 1.0 color keyword names
<http://www.w3.org/TR/css3-color/#svg-color>`_ in *color.<colorname>* format::

    color.yellow
    color.azure
    color.darkseagreen


Color functions
^^^^^^^^^^^^^^^

There are a number of functions that can be used to manipulate colors. These
functions can be invoked on color objects using the *<color>.<function>*
notation::

    #ff8.lighten(0.5)
    color.blue.darken(0.2)
    rgb(11%, 20%, 42%).blend(#fff, 0.5)


The following fuctions can be used on color objects:

.. function:: darken(factor)

    Darkens the color by the given factor. The value of *factor* should be in
    the *0.0-1.0* range and it is clamped to this range if it's not. For
    example::

        color.red.darken(0.5)   -- yields dark red


.. function:: lighten(factor)

    Darkens the color by the given factor. The value of *factor* should be in
    the *0.0-1.0* range and it is clamped to this range if it's not. For
    example::

        color.blue.lighten(0.5)   -- yields light blue


.. function:: blend(destcol, factor)
     
    Blends the color with *destcolor* by a given factor. The value of *factor*
    should be in the *0.0-1.0* range and it is clamped to this range if it's
    not. For example::

        #118833.blend(#fff, 0.8)
        #777.blend(color.red, 0.6)
        baseColor.blend(bgColor, 0.2)

Blending a color with white or black results in a different, less saturated
shade than using the *lighten* and *darken* functions, which might be
preferable in some situations. The following table illustrates the difference
between the two methods for some colors:

TODO image



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




