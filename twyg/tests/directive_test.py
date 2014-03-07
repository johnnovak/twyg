import os, sys, unittest


sys.path.append(os.path.join('..'))

from twyg.config import (ConfigError, tokenize, buildconfig, parse_expr,
                         eval_expr, parsecolor)


# Get & initialise graphics context
from twyg import _init
from twyg.cairowrapper import context as ctx

_init()


class TestEvalExpr(unittest.TestCase):

    def test_valid_longconfig(self):
        config = r"""
-- comment
-- other comment

    [layout]
style                   layout
horizontalBalance       0.5
rootPadX1               50 + depth * 5
rootPadX2               ((50.0 + 10.) * 5 + 10) / 2.000 + 1
rootPadX3                -(10.0 + -.5 * ((4. - 00033) * .32400000 / 6 + 234) * -55.0000) + -(0000.5 + -6) * -(-5 + 1.)
rootPadX4               max(2, depth)
rootPadX5               #ffaa00.lighten(.5)
rootPadX6               #ffaa00.lighten(.4).darken(.2).blend(#fff, 8.8)
rootPadX7               baseColor.lighten(.4)
nodePadX8               50
--nodePadY9               7
branchPadY              15
radialMinNodes          1000
percentColorRGBA        rgba(44%, 100%, 80%, 0.4)
percentColorHSLA        hsla(99, 12%, 74%, 0.330)

 [node] -- stuff
---------------------------------------------------------------------------
{level1}

    style              rect
    fontname            Trebuchet MS
    fontsizes          [21, 15, 13]
    maxTextWidth      230
    textAlign           center
    textPadX            nodeWidth * 0.9
    textPadY            nodeHeight * 0.7
    strokeWidth             depth
    roundness               0.4
    nodeShadowColor         rgba(0, 0, 0, 0.2) -- asdf
    gradientBottomColor     baseColor.darken(-0.04)
    gradientTopColor        baseColor.lighten(0.12).hue(+5)
otherColor              baseColor.blend(bgColor, 0.5).saturation(-10)
otherColor              color.pinksalmon -- asdf
otherColor              #1288f3 --asdf
otherColor              #142bce --asdf
otherColor              hsla(120, 0.4, 0.4, 1.0)

arr0                  [ 1, 2, 3, 4, 5, 6]

arr1                  [ 1, 2, 3,
                          4, 5, 6]

    arr2      [1,2,3,
                    4,5,6
                    ]

arr3                  [
                        1, 2,
            --------------------------------------
                        3, 4
                        ,5, -- some comment
                        6
                        ] -- end

nodecolor               #125588

--
        {level2} -- asdf
    @copy level1


---------------------------------------------------------------------------
[connection]
---------------------------------------------------------------------------
style                   curve
rootLineWidth           2.5
nodeLineWidth           1.5
rootStartWidthFactor    1
nodeStartWidthFactor    1
rootCx1Factor           2.3
nodeCx1Factor           0.6
nodeCx2Factor           0

    [color]
     {level1}
      style                   colorizer
      boxDepthMin             10
      boxDepthMax             10
       boxFillColorFactor      0
         boxBorderColorFactor    -0.15
         arraytest1          [depth, 2]
         arraytest2          [depth, ]
        """

        tokens = tokenize(config)
        config = buildconfig(tokens)

        vars = {
            'depth': 13,
            'baseColor': ctx.color(.5, .25, .125, .5)
        }

        node = config['node']
        level = node['level1']

        e = parse_expr(level['arr0'])
        e = eval_expr(e)
        self.assertEquals([1, 2, 3, 4, 5, 6], e)

        e = parse_expr(level['arr1'])
        e = eval_expr(e)
        self.assertEquals([1, 2, 3, 4, 5, 6], e)

        e = parse_expr(level['arr2'])
        e = eval_expr(e)
        self.assertEquals([1, 2, 3, 4, 5, 6], e)

        e = parse_expr(level['arr3'])
        e = eval_expr(e)
        self.assertEquals([1, 2, 3, 4, 5, 6], e)

        node = config['color']
        level = node['level1']

        e = parse_expr(level['arraytest1'])
        e = eval_expr(e, vars)
        self.assertEquals([13, 2], e)

        e = parse_expr(level['arraytest2'])
        e = eval_expr(e, vars)
        self.assertEquals([13], e)

    def test_valid_levels(self):
        config = r"""
        [layout]
            {level1}
                param1  1

            {level2}
                param2  2

        [node]
            {level1}
                param3  3

            {level2}
                param4  4

            {level3}
                @copy level2
                param4  42
                param5  5

            {level4}
                @copy level3
                param5  52
                param6  6

        [color]
            {level1}
                param7  7
        """

        tokens = tokenize(config)
        config = buildconfig(tokens)

        # ==============================================
        section_names = config.keys()
        self.assertEquals(3, len(section_names))
        self.assertTrue('layout' in section_names)
        self.assertTrue('node' in section_names)
        self.assertTrue('color' in section_names)

        # ==============================================
        layout = config['layout']
        level_names = layout.keys()
        self.assertEquals(2, len(level_names))
        self.assertTrue('level1' in level_names)
        self.assertTrue('level2' in level_names)

        l = layout['level1']
        self.assertEquals(1, len(l))
        e = parse_expr(l['param1'])
        self.assertEquals(1, eval_expr(e))

        l = layout['level2']
        self.assertEquals(1, len(l))
        e = parse_expr(l['param2'])
        self.assertEquals(2, eval_expr(e))

        # ==============================================
        node = config['node']
        level_names = node.keys()
        self.assertEquals(4, len(level_names))
        self.assertTrue('level1' in level_names)
        self.assertTrue('level2' in level_names)
        self.assertTrue('level3' in level_names)
        self.assertTrue('level4' in level_names)

        # ----------------------------------------------
        l = node['level1']
        self.assertEquals(1, len(l))
        e = parse_expr(l['param3'])
        self.assertEquals(3, eval_expr(e))

        # ----------------------------------------------
        l = node['level2']
        self.assertEquals(1, len(l))

        e = parse_expr(l['param4'])
        self.assertEquals(4, eval_expr(e))

        # ----------------------------------------------
        l = node['level3']
        self.assertEquals(2, len(l))
        e = parse_expr(l['param4'])
        self.assertEquals(42, eval_expr(e))

        e = parse_expr(l['param5'])
        self.assertEquals(5, eval_expr(e))

        # ----------------------------------------------
        l = node['level4']
        self.assertEquals(3, len(l))

        e = parse_expr(l['param4'])
        self.assertEquals(42, eval_expr(e))

        e = parse_expr(l['param5'])
        self.assertEquals(52, eval_expr(e))

        e = parse_expr(l['param6'])
        self.assertEquals(6, eval_expr(e))

        # ==============================================
        color = config['color']
        level_names = color.keys()
        self.assertEquals(1, len(level_names))
        self.assertTrue('level1' in level_names)

        l = color['level1']
        self.assertEquals(1, len(l))

        e = parse_expr(l['param7'])
        self.assertEquals(7, eval_expr(e))

    def test_duplicate_level(self):
        config = r"""
        [layout]
            {level1}
                param1  1

            {level1}
                param2  2
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_duplicate_section(self):
        config = r"""
        [layout]
            {level1}
                param1  1
        [layout]
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_start(self):
        config = r"""
        {level1}
        [layout]
                param1  1
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_section_props(self):
        config = r"""
        [layout]
            param1  1
            {level1}
                param2  1
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_section(self):
        config = r"""
        [layout] param1  1
            {level1}
                param2  1
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_level(self):
        config = r"""
        [layout]
            {level1} param2  1
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_directive_syntax(self):
        config = r"""
        [layout]
            {level1}
                param2  1
                @copy {asdf}

        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_level_not_found(self):
        config = r"""
        [layout]
            {level1}
                param2  1
                @copy asdf

        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_directive(self):
        config = r"""
        [node]
        @bullshit
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_missing_directive_params(self):
        config = r"""
        [node]
        @copy
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_property_name(self):
        config = r"""
        [node]
        +
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_property_def_start(self):
        config = r"""
        [node]
        name {asdf}
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_property_def_inside(self):
        config = r"""
        [node]
        name 5 + 3 / {asdf}
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_missing_prop_def(self):
        config = r"""
        [node]
        copy
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_array_nested(self):
        config = r"""
        [node]
        name  [a, [b, c]]
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_array_badend(self):
        config = r"""
        [node]
        name  [a, b, c] s
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_badarray(self):
        config = r"""
        [node]
        name  [a, b, {stuff}]
        """
        tokens = tokenize(config)
        self.assertRaises(ConfigError, buildconfig, tokens)

    def test_invalid_badstring1(self):
        config = r"""
        [node]
        string  "bad string1
        """
        self.assertRaises(ConfigError, tokenize, config)

    def test_invalid_badstring2(self):
        config = r"""
        [node]
        string  'bad string2'
        """
        self.assertRaises(ConfigError, tokenize, config)

    def test_invalid_badstring3(self):
        config = r"""
        [node]
        string  "bad \"string3""
        """
        self.assertRaises(ConfigError, tokenize, config)

    def test_invalid_badstring4(self):
        config = r"""
        [node]
        string  "bad string4\"
        """
        self.assertRaises(ConfigError, tokenize, config)

    def test_invalid_badstring5(self):
        config = r"""
        [node]
        string  \"bad string5\"
        """
        self.assertRaises(ConfigError, tokenize, config)


if __name__ == '__main__':
    unittest.main()

# TODO
# this is valid:
#   someColor #fff
# ...but this should trigger an error:
#   some Color #fff
