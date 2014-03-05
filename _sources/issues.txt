Known issues
============

General
-------

- Some UTF-8 character & font combination cause lockups (typically characters from non-Western languages).

Backends
--------

In general, pixel-exact rendering should not be expected across backends.
There are some differences in how images are rendered with the Cairo and
NodeBox backends:

- Font name resolution works differently (e.g. some fonts can be used in one
  backend but not in the other).
- Font rendering is slightly different (e.g. font baselines are not in the same
  Y-position).
- Shadows look a bit different (NodeBox uses Quartz to render the shadows,
  while when using Cairo, shadows are rasterized by a custom Python algorithm).
- Transparent PDF backgrounds are not possible when using Cairo.
- Shadows are not positioned correctly when outputting SVG files.
- Gradient colors are not exactly the same.

