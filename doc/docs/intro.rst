Introduction
============

Overview
--------

*twyg* lets you visualise arbitrary tree structures in a pretty way. The
appearance of the tree (layout, color, node, connection shapes etc.) is
fully controlled via configuration files in a generative way. This means that
almost all visual properties of the output can be controlled by expressions
that depend on the characteristics of the tree (e.g. the color or shape of a
node can be a function of its hierarchical position in the tree). This allows
for crafting very flexible configurations that can be applied to trees of
arbitrary size and complexity.

Plain-text JSON files describing the tree are expected as input.  These JSON
files only contain the topology of the tree and the text labels of the
individual tree nodes. They do not contain any information on `how` the tree
should be visually rendered; this is entirely described by the
configurations.  The benefit of separating the visual style from the tree data
itself—in a way similar to separating style from content in the case of
CSS and HTML—is that this way one can easily render the same tree in different
visual styles by just applying different configurations to it.

*twyg* comes with an extensive set of default configurations and
colorschemes to get you started. This way, you can get usable results quickly
by just combining the included configuration and colorschemes, then gradually
learn the intricacies of the configuration language to create your own custom
visual styles. Moreover, you can combine both the built-in and your own
configurations in a cascading fashion (akin to CSS) to build up your own
library of custom styles.

Features
--------

- Compatible with Python 2.5, 2.6 and 2.7
- Supports the *Cairo* and *NodeBox1* rendering backends
- 16 visually fine-tuned built-in configurations
- 32 attractive looking colorschemes
- Simple JSON files as input
- PNG, PDF, SVG and PostScript output using the Cairo backend
- Fully customisable node and connection shapes and coloring algorithms
- High-quality font rendering via Cairo
- Gradient and drop shadow support, even in PDF and PostScript files
- Custom human-readable configuration language that allows the visual
  properties of the tree to be defined as expressions of arbitraty complexity
- Ability to cascade configurations and configuration sections
- Full `CSS3 color notation 
  <http://www.w3.org/TR/css3-color/#colorunits>`_ and `SVG 1.0 color keyword
  name <http://www.w3.org/TR/css3-color/#svg-color>`_ support
- Extensive reference documentation

