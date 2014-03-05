Node
====

The *node* configuration section controls the visual appearance of the
nodes, including the size and shape of the nodes, the font used to draw
the node text and so forth.


Common properties
-----------------

The properties below are common to all node styles so they are listed only
once in this section.

Text properties
^^^^^^^^^^^^^^^

.. property:: fontName

    .. propparams:: String "Gill Sans"

    Name of the font to draw the node text with. Normal font weights are
    always used.
    
    .. note:: The font name is usually not portable across different
        operating system and graphics backend combinations and it might need to
        be adjusted for each platform. Different graphics backends and
        operating systems may resolve font names differently, for example the
        font name "Helvetica" might result in a different font being picked up
        by NodeBox on Mac OS X than the by the command line application on
        Windows using the Cairo backend.
        

.. property:: lineHeight

    .. propparams:: Number 1.3
       :values: >0.0

    Line height of the node text expressed as a multiplier of the font size.


.. property:: textAlign

    .. propparams:: Enum auto
        :values: left, right, center, justify, auto

    Alignment of the text within the node shape. The value *auto* aligns the
    text left or right depending on the node's orientation in relation to its
    parent and centers the text in the root node.


.. property:: justifyMinLines

    .. propparams:: Number 5
       :values: >0

    If :ref:property:`textAlign` is set to *justify*, this property
    specifies the minimum number of lines for the full justification to
    take effect.  If the total number of lines is below this value, the
    text will be centered instead.


.. property:: hyphenate

    .. propparams:: Boolean yes

    Controls whether the node text should be hyphenated if it spans multiple
    lines.

    .. note:: Hyphenation is supported for English text only.


.. property:: maxTextWidth

    .. propparams:: Number 240.0
       :values: >0.0

    Maximum width of the node text. If the whole text cannot fit into a
    single line of this width, the text will be broken into multiple
    lines and it will be aligned according to the value of the
    :ref:property:`textAlign` property.


.. property:: textPadX

    .. propparams:: Number fontSize * 1.0
       :values: >0.0

    Horizontal padding between the bounding rectangle of the node text and the
    node shape. It is recommended to set this value proportional to the font
    size.


.. property:: textPadY

    .. propparams:: Number fontSize * 0.45
       :values: >0.0

    Vertical padding between the bounding rectangle of the node text and the
    node shape. It is recommended to set this value proportional to the font
    size.


.. property:: textBaselineCorrection

    .. propparams:: Number -0.2

    Vertical text baseline correction factor expressed as a fraction of the
    font size. Positive values move the baseline downwards, negative upwards.
    The value might need to be adjusted for the font used.

    .. note:: Different graphics backend and operating system combinations
        might require slightly different values for the same font to be
        positioned vertically in the same way.


Stroke properties
^^^^^^^^^^^^^^^^^

.. property:: strokeWidth

    .. propparams:: Number 1.3
       :values: >0.0

    Stroke width of the outline of the node shape. A value of *0.0*
    results in no outline.


Shadow properties
^^^^^^^^^^^^^^^^^

.. note:: Shadows are rendered slightly differently under the NodeBox and Cairo
    backends, although they look quite similar for practical purposes. Turning
    shadows on slows down rendering considerably when using the Cairo backend
    (command line interface). This can be sped up by decreasing the shadow
    rasterisation resolution at the expense of sacrificing some image quality,
    which might not be apparent for light and blurry shadows.

.. warning:: Shadows are positioned incorrectly when using the SVG output with
    the Cairo backend.


.. property:: nodeDrawShadow

    .. propparams:: Boolean no

    Controls whether the node shape casts a shadow.


.. property:: nodeShadowColor

    .. propparams:: Color rgba(0, 0, 0, 0.2)

    Color of the node shadow. Typically, this is specified as an RGBA color
    with a low alpha value to make the shadow somewhat transparent.


.. property:: nodeShadowBlur

    .. propparams:: Number 3.0
       :values: >0.0

    Blur radius of the node shadow. Larger values yield smoother shadows but
    result in longer rendering times (especially with the Cairo backend).


.. property:: nodeShadowOffsX

    .. propparams:: Number 2.5

    Horizontal offset of the node shadow.


.. property:: nodeShadowOffsY

    .. propparams:: Number 2.5

    Vertical offset of the node shadow.


.. property:: textDrawShadow

    .. propparams:: Boolean no

    Controls whether the node text casts a shadow.


.. property:: textShadowColor

    .. propparams:: Color rgba(0, 0, 0, 0.5)

    Color of the text shadow. Typically, this is specified as an RGBA color
    with a low alpha value to make the shadow somewhat transparent.


.. property:: textShadowOffsX

    .. propparams:: Number -0.6

    Horizontal offset of the text shadow.


.. property:: textShadowOffsY

    .. propparams:: Number -0.6

    Vertical offset of the text shadow.



Gradient fill properties
^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: Gradient fill colors appear to be a slightly different under the
    NodeBox and Cairo backends.


.. property:: drawGradient

    .. propparams:: Boolean no

    Controls whether the node shape should be filled using a linear top-down
    gradient.


.. property:: gradientTopColor

    .. propparams:: Color baseColor.lighten(.12)

    Color at the top of the gradient.


.. property:: gradientBottomColor

    .. propparams:: Color baseColor.darken(.04)

    Color at the bottom of the gradient.


Other properties
^^^^^^^^^^^^^^^^

.. property:: connectionAnchorPoint

    .. propparams:: Enum auto
        :values: auto, center

    TODO


'box' style
-----------

The *box* style draws nodes as axonometric three-dimensional boxes.

.. image:: figures/images/nodes-box.png


Properties
^^^^^^^^^^

.. property:: boxOrientation

    .. propparams:: Enum topright
       :values: topleft, topright, bottomleft, bottomright

    Orientation of the three-dimensional depth of the box.


.. property:: boxDepth

    .. propparams:: Number 20 * pow(0.7, depth)
       :values: >0.0

    The three-dimensional depth of the box.


.. property:: horizSideColor

    .. propparams:: Color baseColor.lighten(0.34)

    Color of the horizontal part of the three-dimensional depth of the box.


.. property:: vertSideColor

    .. propparams:: Color baseColor.lighten(0.12)

    Color of the vertical part of the three-dimensional depth of the box.


.. property:: strokeColor

    .. propparams:: Color baseColor

    Stroke color of the wireframe of the box. Back lines are not drawn.



'line' style
------------

The *line* style is a special node shape style that draws a line below or above
the node text so that it appears as a continuation of the line connecting the
nodes.

.. image:: figures/images/nodes-line.png

The following examples illustrate the use the *line* style:

TODO


Properties
^^^^^^^^^^

None.



'oval' style
------------

The *oval* style draws nodes as oval shapes.

.. image:: figures/images/nodes-oval.png


Properties
^^^^^^^^^^

.. property:: aspectRatio

    .. propparams:: Number 1.0
       :values: >0.0

    Initial aspect ratio of the oval (the ratio of the width and the height of
    the oval). Values less than *1.0* yield a vertically oriented oval shape,
    values greater than *1.0* a horizontally oriented oval, and *1.0* a circle.


.. property:: maxWidth

    .. propparams:: Number 400.0
       :values: >0.0

    Maximum width the oval is allowed to reach without changing its aspect
    ratio. Once the width limit is reached, the aspect ratio is progressively
    decreased until the full node text fits into the node shape.



'poly' style
------------

The *poly* style draws nodes as n-sided regular polygons (all sides have the
same length and all angles are equal in measure).

.. image:: figures/images/nodes-poly.png


Properties
^^^^^^^^^^

.. property:: numSides

    .. propparams:: Number 6
       :values: >0

    Number of sides of the regular polygon.


.. property:: rotation

    .. propparams:: Number 0

    Rotation of the polygon around its center in degrees.



'rect' style
------------

The *rect* style draws nodes as rectangular shapes that can be either
completely square (first example) or can have rounded corners drawn in
different rounding styles (last two examples).

.. image:: figures/images/nodes-rect.png


Properties
^^^^^^^^^^

.. property:: roundingStyle

    .. propparams:: Enum screen
       :values: screen, arc

    Controls the rounding style of the rectangle. *screen* results in a
    shape similar to an old CRT television screen, *arc* draws a
    rectangle with rounded corners using quarter circle arc segments.

    .. figure:: figures/images/nodes-rect-roundingStyle-a.png
       :alt: screen

       screen


    .. figure:: figures/images/nodes-rect-roundingStyle-b.png
       :alt: arc

       arc


.. property:: roundness

    .. propparams:: Number 1.0
       :values: 0.0–1.0

    Rectangle roundess factor if :ref:property:`roundingStyle` is set to
    *screen*. A value of *0.0* yields completely square corners and
    *1.0* fully rounded ones.

    .. figure:: figures/images/nodes-rect-roundness-a.png
       :alt: roundness = 0

       roundness = 0


    .. figure:: figures/images/nodes-rect-roundness-b.png
       :alt: roundness = 0.5

       roundness = 0.5


    .. figure:: figures/images/nodes-rect-roundness-c.png
       :alt: roundness = 1.0

       roundness = 1.0


.. property:: cornerRadius

    .. propparams:: Number 5.0
       :values: >0.0

    If :ref:property:`roundingStyle` is set to *arc*, the rectangle
    corners are drawn using quarter circle arcs having this radius (in
    points). The radius is capped at half the node's height or width
    (whichever is lower) to prevent self-overlapping curves. This lends
    itself to a neat trick to draw capsule-like node shapes by setting
    the corner radius to a very large value (last example).

    .. figure:: figures/images/nodes-rect-cornerRadius-a.png
       :alt: cornerRadius = 5

       cornerRadius = 5


    .. figure:: figures/images/nodes-rect-cornerRadius-b.png
       :alt: cornerRadius = 10

       cornerRadius = 10


    .. figure:: figures/images/nodes-rect-cornerRadius-c.png
       :alt: cornerRadius = 1000

       cornerRadius = 1000

