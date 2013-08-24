Configuration
=============

Configurations are plain text files with a ``.twg`` extension. They describe
the visual appearance of the tree, such as the shape, color and positioning of
the nodes and connections, the font used to draw the text inside the nodes and
so on. Configuration files do not contain any tree data --- they only describe
`how` the trees should be drawn and these instructions can then be applied to
arbitrary tree data files.  

Configurations have the following structure:

* Four mandatory :ref:`section definitions <sections>` at the top level (layout, nodes, connection and colors).
* Each section definition must contain either

  * a list of :ref:`property definitions <properties>`
  * or one or more :ref:`level definitions <levels>` containing lists of
    property definitions.

* Property definitions are name-value pairs separated by whitespace characters.
* :ref:`Directives <directives>` that trigger special processing can also
  appear where properties are allowed.

All names in a configuration are case sensitive. Extra blank lines and
whitespace characters are not significant.  Line comments can be included by
using the ``--`` marker (two dash characters).

The following is an example of a simple configuration file::

    [layout]                                     -- layout section start marker
        style                 layout             -- layout style
        rootPadX              70                 -- property definition; constant
                                                
    [node]                                       -- node section start marker
        style                 rect               -- node style
        textPadY              fontSize * 0.7     -- property definition; expression
                                                
    [connection]                                 -- connection section start marker
      {default}                                  -- 'default' level start marker
        style                 curve              -- connection style
        nodeLineWidthStart    1.5               
        nodeLineWidthEnd      1.5               
                                                
      {root}                                     -- 'root' level start marker
        @copy                 default            -- copy directive
        levelDepthMax         0                  -- level selector
        nodeLineWidthEnd      3.5                -- override nodeLineWidthEnd
                                                
    [color]                                      -- color section start marker
        style                 colorizer          -- color style
        @include              "mycolor.twg"      -- include directive


.. _sections:

Sections
--------

Sections hold a set of property definitions together that control one visual
aspect of a tree. There are four section types in total:

  ``layout``
    Controls the positioning of the nodes.

  ``node``
    Controls how the individual nodes are drawn.

  ``connection``
    Controls how the shapes connecting the nodes are drawn.

  ``color``
    Defines the colors used for all drawing operations.

The start of the sections are denoted by section markers, which are written as
the name of the section in square brackets (e.g. ``[node]``). Everything that
appears below a section marker belongs to that section until another section
start marker is encountered. For example::

    [layout]                                     -- layout section start marker
        style                 layout             
        rootPadX              70                 
                                                
    [node]                                       -- node section start marker
        style                 rect               
        textPadY              fontSize * 0.7     

All four section must be present in the configuration and they cannot appear
more than once.


.. _levels:

Levels
------

In the examples above, we defined an uniform visual style for all nodes,
connections, colorings etc.  But many times it is desirable to style elements
of the tree differently based on their position in the graph. For example, the
root node, the leaves and the rest of the nodes could appear in three distinct
visual styles.  Or all nodes at depth 1 could have a certain style, nodes at
depth 2 another one, and so on. 

By using level definitions within the section definitions, it is possible to
further refine the visual appearance of the different elements of the tree.
Levels can appear in the *node*, *connection* and *color* sections with the
following syntax::

    [section]
        {levelname}
           ...
           property definitions
           ...

In this example, the root node is drawn as an octagonal polygon, the leaf nodes
as ovals, and the rest of the nodes as rectangle::

    [node]
      {root}
        levelDepthMax           0
        style                   poly
        numSides                8

      {leaf}
        levelNumChildrenMax     0
        style                   oval

      {normal}
        style                   rect


Level selectors
^^^^^^^^^^^^^^^

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

*Select root node only* ::

    {root}
      levelDepthMax         0


*Select all leaf nodes* ::

    {leaf}
      levelNumChildrenMax   0


*Select leaf nodes at depth 2 at least* ::

    {leaf}
      levelDepthMin         2
      levelNumChildrenMax   0


.. _directives:

Directives
----------

Directives can appear within section and level definitions just like regular
properties but they have special meaning.

.. directive:: @copy

    Copy all property definitions from another level into the current one
    within the same section. The directive is only allowed to appear in level
    definitions. The level *<levelname>* does not have to be defined in the
    same file where the *@copy* directive appears in, it can also come from
    another configuration file that was included previously (see
    :ref:directive:`@include` ).

    The purpose of the *@level* directive is to avoid duplication of
    configuration contents where mostly similar, but slightly different sets of
    property definitions need to be applied to two (or more) distinct sets of
    entities.  For example, one could define a default style that applies to
    all nodes, then apply the same style to the leaf nodes with a few property
    definitions changed. In this sense, the directive achieves something
    similar to the concept of inheritance in object-oriented programming
    languages.

    Note that as the contents of the configuration files are evaluated line by
    line from top to bottom, it is possible to override the copied properties
    by redefining them after a *@copy* directive, as shown in the example
    below.

    In this example, all nodes are drawn as rounded rectangles, except for the
    root node, which is drawn as a regular rectangle::

        [node]
          {normal}
            style                   rect
            roundness               1.0

          {root}
            @copy                   normal
            levelDepthMax           0
            roundness               0.0


.. directive:: @include

    Include the contents of another configuration file into the current
    configuration. The most natural way to think about this is that the line
    containing the *@include* directive is replaced with the contents of
    *<configname>* and then the parsing continues. There is no limit to the
    nesting depth of configuration files, but obviously two configuration
    cannot include each other. If such circular reference is encountered, an
    error is raised and the execution stops.

    The search order for the configuration file is the following:

    * The current directory (the directory the main Python script was
      started in)
    * ``$TWYG_USER/configs``
    * ``$TWYG_HOME/configs``

    If the configuration file cannot be found in either of these locations, an
    error is raised and the execution stops.

    For example::

        [connection]
            @include                "connections/style1.twg"
            cornerRadius            40
            junctionRadius          17

    In this example, the included configuration file will be searched in the
    following locations:

    * ``connections/style1.twg``
    * ``$TWYG_USER/configs/connections/style1.twg``
    * ``$TWYG_HOME/configs/connections/style1.twg``


.. _properties:

Properties
----------

Property definitions are name-value pairs separated by at least one whitespace
character. Each configuration section and style has a distinct set of
predefined property names. For a detailed description of all available
properties see the :ref:`properties-reference`.

Property values can be either simple literal values::

        rootPadX        70

or expressions or arbitrary complexity::

        fontSize        max(10, round(21 / sqrt(depth + 1)))

The important thing to remember is that the property value starts at the first
non-whitespace character after the property name and it cannot span multiple
lines.

There is an exception to this rule; array property values are allowed to span
multiple lines::

    nodeColors      [#af8700, #d75f00, #d70000, #af005f,
                     #5f5faf, #0087ff, #00afaf, #5f8700]

Property value types
^^^^^^^^^^^^^^^^^^^^

Every property has a type, which is one of the following:

*Number*
    A numeric value::

      level     5
      width     103.2
      stuff     -3.1516

*String*
    A string in double-quotes. Double-quote characters within a string have to be escaped with a backslash (\)::

      fontName  "Source Sans Pro"
      name      "double-quotes: \"\""

*Boolean*
    Used for turning a specific feature on or off. Valid values are: 

    * ``yes``, ``true`` or ``1``
    * ``no``,  ``false`` or ``0``

*Color*
    Defines a color. See :ref:`colors` for more information.

*Enum*
    Property specific list of predefined values. See the
    :ref:`properties-reference` for details.

*Array*
    TODO


Variables
^^^^^^^^^

The following variables are available in property definition expressions:

.. hlist::
    :columns: 4

    * *x*
    * *y*
    * *width*
    * *height*

    * *bboxWidth*
    * *bboxHeight*
    * *textWidth*
    * *textHeight*

    * *maxTextWidth*
    * *lineHeight*
    * *fontSize*
    * *fontColor*

    * *bgColor*
    * *baseColor*
    * *fillColor*
    * *strokeColor*

All variables contain numeric values, except the ones ending with *Color*.
TODO: some explanation why aren't they always available 


Mathematical functions
^^^^^^^^^^^^^^^^^^^^^^

The following mathematical functions can be used in property expressions:

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


.. _colors:


Colors
^^^^^^

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

For a comprehensive description of CSS3 color notation refer to the `CSS Color
Module Level 3 <http://www.w3.org/TR/css3-color/#colorunits>`_ specification.


Color functions
^^^^^^^^^^^^^^^

There are a number of functions that can be used to manipulate colors. These
functions can be invoked using the *<color>.<function>* notation. For example::

    #ff8.lighten(0.5)
    color.blue.darken(0.2)
    rgb(11%, 20%, 42%).blend(#fff, 0.5)

The following color manipulation functions are available. The parameter *factor*
should be between *0.0-1.0* in all cases and it is clamped to this range if it
lies outside.


.. function:: darken(factor)

    Darkens the color by the given factor. ::

        color.red.darken(0.5)
        #48a70f.darken(0.3)


.. function:: lighten(factor)

    Darkens the color by the given factor.  ::

        color.fuchsia.lighten(0.3)
        hsla(88, 30%, 68%, 0.7).lighten(.7)


.. function:: blend(destcolor, factor)
     
    Blends the color (source color) with *destcolor* by the given factor. A
    *factor* of *1.0* will result in the destination color and *0.0* in the
    source color. ::

        #118833.blend(#fff, 0.8)
        #777.blend(color.red, 0.6)
        baseColor.blend(bgColor, 0.2)

.. tip:: The brightness of a color can be changed in two ways:
    
    * using the :py:func:`darken` and :py:func:`lighten` functions
    * blending the color with black or white

    The blending method result in less saturated shades which might be
    preferable in some situations. The following table illustrates the
    difference between the two methods:

    .. image:: figures/images/color-blending.png
       :align: center


