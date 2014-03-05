Layout
======

The *layout* section controls the positioning of the individual nodes within
the tree.


.. property:: horizontalBalance

    .. propparams:: Number 0.5

    Controls the left-right distribution of the root node's children.  A values
    of *0.0* aligns all nodes to the right and a values of *1.0* results in all
    nodes aligned to the left.  *0.5* results in nodes balanced evenly between
    left and right.


.. property:: verticalAlignFactor

    .. propparams:: Number 0.5

    Vertical align factor.  A value of *0.0* aligns all nodes to the top, *0.5*
    center the nodes vertically and *1.0* aligns them all to the bottom.


.. property:: rootPadX

    .. propparams:: Number 160

    Horizontal padding around the root node.


.. property:: nodePadX

    .. propparams:: Number 30.0

    Horizontal padding between the non-root nodes.


.. property:: nodePadY

    .. propparams:: Number 8.0

    Vertical padding between the nodes.


.. property:: branchPadY

    .. propparams:: Number 25.0

    Vertical padding between child node groups.


.. property:: sameWidthSiblings

    .. propparams:: Boolean yes

    Controls whether all sibling nodes should have the same width.


.. property:: snapParentToChildren

    .. propparams:: Boolean no

    Controls whether the connection point of the child nodes should be
    snapped to the parent's connection point.


.. property:: snapToHalfPositions

    .. propparams:: Boolean no

    Controls whether snapping halfway between two connection points is
    allowed.


.. property:: radialMinNodes

    .. propparams:: Number 3

    Minimum number of siblings for arc node placement.


.. property:: radialFactor

    .. propparams:: Number 2.2

    Roundness of the arc node placement.

