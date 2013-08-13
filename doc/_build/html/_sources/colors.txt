Colors
======

.. property:: horizontalBalance

    Controls the left-right distribution of the root node's children:

      0.0 - all nodes to the right
      0.5 - nodes evenly balanced to left and right
      1.0 - all nodes to the left

    .. propparams:: Number 0.5


.. property:: colorscheme

    Colorscheme to use.

    .. propparams:: String "mint"


.. property:: fillColor

    Fill color of the node shape.

    .. propparams:: Color baseColor


.. property:: strokeColor

    Stroke color of the node shape

    .. propparams:: Color baseColor


.. property:: connectionColor

    Color of the connection that connects the nodes

    .. propparams:: Color baseColor


.. property:: fontColor

    Color of the text label that appears inside the node

    .. propparams:: Color bgColor


.. property:: fontColorAuto

    Controls whether the color of the text label should be determined
    automatically. If set to yes, the color is automatically determined,
    if set to no, the fontColor property is used.

    .. propparams:: Boolean yes


.. property:: fontColorAutoDark

    Dark variant of the automatic text label color

    .. propparams:: Color baseColor.darken(.35)


.. property:: fontColorAutoLight

    Light variant of the automatic text label color

    .. propparams:: Color baseColor.blend(color.white, .8)


.. property:: fontColorAutoThreshold

    Minimum brightness difference between the color of the text label
    and its background. The text label color variant is choosen based on
    this threshold.

    .. propparams:: Number 0.3

