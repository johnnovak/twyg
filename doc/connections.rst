Connections
===========

These properties are common to all node drawers. Lorem ipsum dolor
sit amet, consectetur adipiscing elit. Etiam cursus sit amet justo nec
lacinia. Pellentesque id hendrerit eros. Suspendisse a nunc enim.
Quisque vitae velit dolor.



'curve' style
-------------


Properties
^^^^^^^^^^

.. property:: nodeLineWidthStart

    Start width of the connection curve

    .. propparams:: Number 9.8    


.. property:: nodeLineWidthEnd

    End width of the connection curve

    .. propparams:: Number 1.4


.. property:: nodeCx1Factor           0.7

    Control point 1 X-factor of the connection curve

    .. propparams:: Number 0.7
    

.. property:: nodeCx2Factor

    Control point 2 X-factor of the connection curve

    .. propparams:: Number .28


.. property:: nodeCy1Factor

    Control point 1 Y-factor of the connection curve

    .. propparams:: Number 0.0


.. property:: nodeCy2Factor

    Control point 2 Y-factor of the connection curve

    .. propparams:: Number 0.0



'junction' style
----------------


Properties
^^^^^^^^^^

.. property:: lineWidth

    Width of the connection line

    .. propparams:: Number 4.0


.. property:: junctionXFactor

    Horizontal position of the junction sign in relation to the total horizontal
    width of the connection line

      0.0     - at the parent node
      0.0-1.0 - between the parent and child nodes
      1.0     - at the child node

    .. propparams:: Number 0.4


.. property:: cornerStyle

    Style of the corners of the connection lines.

    .. propparams:: Enum rounded
       :values: square | beveled | rounded


.. property:: cornerRadius

    Radius of the corners of the connection lines (has no effect with the 
    square corner style).

    .. propparams:: Number 12.0


.. property:: junctionStyle

    Style of the junction point.

    .. propparams:: Enum disc
       :values: none | square | disc | diamond.


.. property:: junctionRadius

    Radius of the junction point.

    .. propparams:: Number 10.0


.. property:: junctionFillColor

    Fill color of the junction point.

    .. propparams:: Color baseColor



.. property:: junctionStrokeWidth

    Stroke width of the junction sign.

    .. propparams:: Number 2.0


.. property:: junctionStrokeColor

    Stroke color of the junction sign.

    .. propparams:: Color baseColor


.. property:: junctionSign

    Style of the sign inside the junction point.

    .. propparams:: Enum none
       :values: none | plus | minus


.. property:: junctionSignSize

    Size of the junction sign.

    .. propparams:: Number 10.0


.. property:: junctionSignStrokeWidth

    Stroke width of the junction sign.

    .. propparams:: Number 2.0


.. property:: junctionSignColor       

    Color of the junction sign.

    .. propparams:: Color baseColor.blend(bgColor, .7)

