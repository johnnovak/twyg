import os, sys, unittest


sys.path.append(os.path.join('..'))

from twyg.config import (ConfigError, tokenize, buildconfig, parse_expr,
                         eval_expr, parsecolor)


# Get & initialise graphics context
from twyg import _init
from twyg.cairowrapper import context as ctx

_init()


class TestEvalExpr(unittest.TestCase):

    def test_validexpressions(self):
        config = r"""
        [node]
        test0       42
        test1       50 + depth * 5
        test2       ((50.0 + 10.) * 5 + 10) / 2.000 + 1
        test3       -(10.0 + -.5 * ((4. - 00033) * .32400000 / 6 + 234) * -55.0000) + -(0000.5 + -6) * -(-5 + 1.)
        test4       max(1+1, depth + sqrt(2*+2) * (floor(1.9 * (+1+1)) + ceil(+.6/+02) - .5))
        test5       foo.bar / 2
        test6       foo.func(sqrt(121) - 1)
        test7       #ff8844.lighten(.5)
        test8       #000000.lighten(.8).darken(.8).blend(#48f, 0.5)
        test9       baseColor.blend(#000, 0.5)
        test10      color.pink
        test11      [-1 * -1, sqrt(9) - 1, 2 * (1 + .5), pow(2, 2)]
        test12      color.white.blend(#000, .25)
        test13      [#111, #222222, #333, #444444]
        test14      -depth+-3
        test15      "some string !@#$%^&*()_+-=[]{},.<>/?;:'`~"
        test16      "\"string\" within a string... and \"yet another example\""
        test17      1 / 2
        test18      1 / 2.
        """

        tokens = tokenize(config)
        config = buildconfig(tokens)

        class Foo:
            pass

        f = Foo()
        f.bar = 42
        f.func = lambda x: x * 2

        vars = {
            'depth': 13,
            'foo': f,
            'baseColor': ctx.color(.5, .25, .125, .5)
        }

        node = config['node']

        e = parse_expr(node['test0'])
        e = eval_expr(e, vars)
        self.assertEquals(42, e)

        e = parse_expr(node['test1'])
        e = eval_expr(e, vars)
        self.assertEquals(115, e)

        e = parse_expr(node['test2'])
        e = eval_expr(e, vars)
        self.assertEquals(156, e)

        e = parse_expr(node['test3'])
        e = eval_expr(e, vars)
        self.assertTrue(abs(e - (-6379.9349999999995)) < 1e-14)

        e = parse_expr(node['test4'])
        e = eval_expr(e, vars)
        self.assertEquals(20, e)

        e = parse_expr(node['test5'])
        e = eval_expr(e, vars)
        self.assertEquals(21, e)

        e = parse_expr(node['test6'])
        e = eval_expr(e, vars)
        self.assertEquals(20, e)

        e = parse_expr(node['test7'])
        e = eval_expr(e, vars)
        self.assertEquals('Color(r=1.000, g=0.533, b=0.267, a=1.000)', str(e))

        e = parse_expr(node['test8'])
        e = eval_expr(e, vars)
        self.assertEquals('Color(r=0.133, g=0.267, b=0.500, a=1.000)', str(e))

        e = parse_expr(node['test9'])
        e = eval_expr(e, vars)
        self.assertEquals('Color(r=0.250, g=0.125, b=0.062, a=0.750)', str(e))

        e = parse_expr(node['test10'])
        e = eval_expr(e, vars)
        self.assertEquals('Color(r=1.000, g=0.753, b=0.796, a=1.000)', str(e))

        e = parse_expr(node['test11'])
        e = eval_expr(e, vars)
        self.assertEquals([1.0, 2.0, 3.0, 4.0], e)

        e = parse_expr(node['test12'])
        e = eval_expr(e, vars)
        self.assertEquals('Color(r=0.750, g=0.750, b=0.750, a=1.000)', str(e))

        e = parse_expr(node['test13'])
        actual = eval_expr(e, vars)
        expected = [parsecolor(None, '#111'), parsecolor(None, '#222222'),
                    parsecolor(None, '#333'), parsecolor(None, '#444444')]
        self.assertEquals(len(expected), len(actual))
        for i in range(len(expected)):
            self.assertEquals(str(expected[i]), str(actual[i]))

        e = parse_expr(node['test14'])
        e = eval_expr(e, vars)
        self.assertEquals(-16, e)

        e = parse_expr(node['test15'])
        e = eval_expr(e, vars)
        self.assertEquals("some string !@#$%^&*()_+-=[]{},.<>/?;:'`~", e)

        e = parse_expr(node['test16'])
        e = eval_expr(e, vars)
        self.assertEquals('"string" within a string... and "yet another example"', e)

        e = parse_expr(node['test17'])
        e = eval_expr(e, vars)
        self.assertEquals(e, .5)

        e = parse_expr(node['test18'])
        e = eval_expr(e, vars)
        self.assertEquals(e, .5)


    def test_invalidexpressions(self):
        config = r"""
        [node]
        test0       42 5
        test1       (42))
        test2       stuff
        test3       color.asdf
        test4       func(1111)
        test5       #555 * 5
        test6       #ff00ff / 333
        test7       baseColor.blend(#fff, baseColor)
        test8       sqrt(#fff)
        test9       -#ff00ff
        test10      +#ff00ff
        test11      baseColor.qwer(111)
        test12      baseColor.lighten
        test13      baseColor.lighten + 5
        test14      max
        test15      max.adsf
        test16      (
        test17      5 +
        test18      5 + (
        test19      (3 + 5 * 3
        test20      .
        test21      max(
        test22      color.pink[
        test23      color.pink.lighten.3
        test24      "string" abc
        test25      "some \"other\" string" "333"
        test26      3 + "a"
        test27      sqrt("abcd")
        test28      color #fff
        """

        tokens = tokenize(config)
        config = buildconfig(tokens)

        vars = {
            'depth': 13,
            'baseColor': ctx.color(.5, .25, .125, .5)
        }

        node = config['node']

        self.assertRaises(ConfigError, parse_expr, node['test0'])
        self.assertRaises(ConfigError, parse_expr, node['test1'])

        e = parse_expr(node['test2'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test3'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test4'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test5'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test6'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test7'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test8'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test9'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test10'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test11'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test12'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test13'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test14'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test15'])
        self.assertRaises(ConfigError, eval_expr, e)

        self.assertRaises(ConfigError, parse_expr, node['test16'])
        self.assertRaises(ConfigError, parse_expr, node['test17'])
        self.assertRaises(ConfigError, parse_expr, node['test18'])
        self.assertRaises(ConfigError, parse_expr, node['test19'])
        self.assertRaises(ConfigError, parse_expr, node['test20'])
        self.assertRaises(ConfigError, parse_expr, node['test21'])
        self.assertRaises(ConfigError, parse_expr, node['test22'])
        self.assertRaises(ConfigError, parse_expr, node['test23'])
        self.assertRaises(ConfigError, parse_expr, node['test24'])
        self.assertRaises(ConfigError, parse_expr, node['test25'])

        e = parse_expr(node['test26'])
        self.assertRaises(ConfigError, eval_expr, e)

        e = parse_expr(node['test27'])
        self.assertRaises(ConfigError, eval_expr, e)

        self.assertRaises(ConfigError, parse_expr, node['test28'])


if __name__ == '__main__':
    unittest.main()

