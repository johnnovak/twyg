Nodes
=====

These properties are common to all node drawers. Lorem ipsum dolor
sit amet, consectetur adipiscing elit. Etiam cursus sit amet justo nec
lacinia. Pellentesque id hendrerit eros. Suspendisse a nunc enim.
Quisque vitae velit dolor.

Vivamus aliquam fringilla metus, sit amet tempor lectus pretium non.
Integer et tempor eros. Donec posuere dignissim nulla, non rutrum ipsum
gravida ut. Maecenas nec lectus eget metus congue blandit. Suspendisse
sed tortor vel neque vestibulum iaculis nec non mi. Nam porttitor
vehicula pharetra.


Common properties
-----------------

The properties below apply to all node styles.

Text properties
^^^^^^^^^^^^^^^

.. property:: fontName

    Name of the font used to draw the text in the node.

    .. propparams:: String "Gill Sans"


.. property:: lineHeight

    Lineheight of the node text expressed as a multiplier of the font size.

    .. propparams:: Number 1.3


.. property:: textAlign

    Alignment of the text within the node. The value <em>auto</em>
    aligns the text left, right or center, depending on the node's
    orientation (center is used for the root node).

    .. propparams:: Enum auto
        :values: left | right | center | justify | auto


.. property:: justifyMinLines

    Minimum number of lines for the <em>justify</em> text alignment to take
    effect. If the total number of lines is less than this value, the text will
    be centered instead.

    .. propparams:: Number 5


.. property:: hyphenate

    Controls whether the node text is hyphenated.

    .. propparams:: Boolean yes


.. property:: maxTextWidth

    Maximum text width inside nodes.

    .. propparams:: Number 240.0


.. property:: textPadX

    Horizontal padding around the bounding box of the node text.

    .. propparams:: Number fontSize * 1.0


.. property:: textPadY

    Vertical padding around the bounding box of the node text.

    .. propparams:: Number fontSize * 0.45


.. property:: textBaselineCorrection

    Node text baseline correction factor.

    .. propparams:: Number -0.2


Stroke properties
^^^^^^^^^^^^^^^^^

.. property:: strokeWidth

    Stroke width of the outline of the node shape.

    .. propparams:: Number 1.3


Node shadow properties
^^^^^^^^^^^^^^^^^^^^^^

.. property:: nodeDrawShadow

    Controls whether the node shape casts a shadow.

    .. propparams:: Boolean no


.. property:: nodeShadowColor

    Node shadow color.

    .. propparams:: Color rgba(0, 0, 0, 0.2)


.. property:: nodeShadowBlur

    Node shadow blur radius.

    .. propparams:: Number 3.0


.. property:: nodeShadowOffsX

    Horizontal offset of the node shadow.

    .. propparams:: Number 2.5


.. property:: nodeShadowOffsY

    Vertical offset of the node shadow.

    .. propparams:: Number 2.5


.. property:: textDrawShadow

    Controls whether the node text casts a shadow.

    .. propparams:: Boolean no


Text shadow properties
^^^^^^^^^^^^^^^^^^^^^^

.. property:: textShadowColor

    Text shadow color.

    .. propparams:: Color rgba(0, 0, 0, 0.5)


.. property:: textShadowOffsX

    Horizontal offset of the text shadow.

    .. propparams:: Number -0.6


.. property:: textShadowOffsY

    Vertical offset of the text shadow.

    .. propparams:: Number -0.6


.. property:: drawGradient

    Controls whether the node shape should be filled using a linear top-down
    gradient.

    .. propparams:: Boolean no


.. property:: gradientTopColor

    Color of the top of the node if the node shade is filled with a gradient.

    .. propparams:: Color baseColor.lighten(.12)


.. property:: gradientBottomColor

    Color of the bottom of the node if the node shade is filled with a
    gradient.

    .. propparams:: Color baseColor.darken(.04)



'box' style
-----------

Properties
^^^^^^^^^^

.. property:: boxOrientation

    3D orientation of the box.

    .. propparams:: Enum topright
       :values: topleft | topright | bottomleft | bottomright


.. property:: boxDepth

    3D depth of the box.

    .. propparams:: Number 20 * pow(0.7, depth)


.. property:: horizSideColor

    Color of the horizontal side of the 3D box.

    .. propparams:: Color baseColor.lighten(0.34)


.. property:: vertSideColor

    Color of the vertical side of the 3D box.

    .. propparams:: Color baseColor.lighten(0.12)


.. property:: strokeColor

    Stroke color of the box.

    .. propparams:: Color baseColor



'line' style
------------

Properties
^^^^^^^^^^

None.



'oval' style
------------

Properties
^^^^^^^^^^

.. property:: aspectRatio

    Initial aspect ratio of the oval.

    .. propparams:: Number 1.0


.. property:: maxWidth

    Maximum width of the oval (the initial aspect ratio is kept until
    this width is reached).

    .. propparams:: Number 400.0



'poly' style
------------

Properties
^^^^^^^^^^

.. property:: numSides

    Number of sides of the regular polygon

    .. propparams:: Number 6


.. property:: rotation

    Rotation around the center point

    .. propparams:: Number 0



'rect' style
------------

Properties
^^^^^^^^^^

.. property:: roundness

    Rectangle roundess (must be between 0.0 and 1.0)

    .. propparams:: Number 1.0


.. property:: cornerRadius

    Corner radius if rounding style is 'arc'.

    .. propparams:: Number 5.0


.. property:: roundingStyle           screen

    Rectangle roundng style.

    .. propparams:: Enum screen
       :values: screen, arc

