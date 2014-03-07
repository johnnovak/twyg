import os, sys, unittest


sys.path.append(os.path.join('..'))

from twyg.css3colors import color_to_rgba, rgba_to_color


class TestCSS3Colors(unittest.TestCase):

    def test_valid(self):
        r, g, b, a = color_to_rgba('aquamarine')
        c = rgba_to_color(r, g, b, a, format='rgb')
        self.assertEquals('rgb(127, 255, 212)', c)

        r, g, b, a = color_to_rgba('000')
        c = rgba_to_color(r, g, b, a, format='hex')
        self.assertEquals('#000000', c)

        r, g, b, a = color_to_rgba('    000')
        c = rgba_to_color(r, g, b, a, format='hex')
        self.assertEquals('#000000', c)

        r, g, b, a = color_to_rgba('#123')
        c = rgba_to_color(r, g, b, a, format='hex')
        self.assertEquals('#112233', c)

        r, g, b, a = color_to_rgba('   #123')
        c = rgba_to_color(r, g, b, a, format='hex')
        self.assertEquals('#112233', c)

        r, g, b, a = color_to_rgba('#deadbe')
        c = rgba_to_color(r, g, b, a, format='hex')
        self.assertEquals('#deadbe', c)

        r, g, b, a = color_to_rgba('#DEaDbE')
        c = rgba_to_color(r, g, b, a, format='hex')
        self.assertEquals('#deadbe', c)

        r, g, b, a = color_to_rgba('deadbe')
        c = rgba_to_color(r, g, b, a, format='hex')
        self.assertEquals('#deadbe', c)

        r, g, b, a = color_to_rgba('deADBE')
        c = rgba_to_color(r, g, b, a, format='hex')
        self.assertEquals('#deadbe', c)

        r, g, b, a = color_to_rgba('rgb(11, 22, 44)')
        c = rgba_to_color(r, g, b, a, format='rgb')
        self.assertEquals('rgb(11, 22, 44)', c)

        r, g, b, a = color_to_rgba('rgb(000011, 022, 00044)')
        c = rgba_to_color(r, g, b, a, format='rgb')
        self.assertEquals('rgb(11, 22, 44)', c)

        r, g, b, a = color_to_rgba('rgba(256, -1, 79, .4)')
        c = rgba_to_color(r, g, b, a, format='rgba')
        self.assertEquals('rgba(255, 0, 79, 0.400)', c)

        r, g, b, a = color_to_rgba('rgb(11%, 22%, 44%)')
        c = rgba_to_color(r, g, b, a, format='rgb_p')
        self.assertEquals('rgb(11%, 22%, 44%)', c)

        r, g, b, a = color_to_rgba('rgba(11%, 122%, -44%, -100)')
        c = rgba_to_color(r, g, b, a, format='rgba_p')
        self.assertEquals('rgba(11%, 100%, 0%, 0.000)', c)

        r, g, b, a = color_to_rgba('   rgba(   11%,     122%,  -44%,  -100  )   ')
        c = rgba_to_color(r, g, b, a, format='rgba_p')
        self.assertEquals('rgba(11%, 100%, 0%, 0.000)', c)

        r, g, b, a = color_to_rgba('hsl(130, 30%, +80%)')
        c = rgba_to_color(r, g, b, a, format='hsl')
        self.assertEquals('hsl(130, 30%, 80%)', c)

        r, g, b, a = color_to_rgba('hsla(+99, 12%, 74%, +.33)')
        c = rgba_to_color(r, g, b, a, format='hsla')
        self.assertEquals('hsla(99, 12%, 74%, 0.330)', c)

        r, g, b, a = color_to_rgba('  hsla(  +000099  , 000012% , 074%  , .330000  )   ')
        c = rgba_to_color(r, g, b, a, format='hsla')
        self.assertEquals('hsla(99, 12%, 74%, 0.330)', c)

    def test_invalid(self):
        self.assertRaises(ValueError, color_to_rgba, 'fuchsiax')

        self.assertRaises(ValueError, color_to_rgba, '5')
        self.assertRaises(ValueError, color_to_rgba, 'rgb()')
        self.assertRaises(ValueError, color_to_rgba, 'rgba()')
        self.assertRaises(ValueError, color_to_rgba, 'rgba()')

        self.assertRaises(ValueError,
                          color_to_rgba, 'rgb(64., 128, 255)')

        self.assertRaises(ValueError,
                          color_to_rgba, 'rgba(64, 128, 255,)')

        self.assertRaises(ValueError,
                          color_to_rgba, 'rgb(++64, 128, 255)')

        self.assertRaises(ValueError,
                          color_to_rgba, 'rgba(  -64   , +128 ,     255., +000.5 )')

        self.assertRaises(ValueError,
                          color_to_rgba, 'rgb(25%, 50, 100%)')

        self.assertRaises(ValueError,
                          color_to_rgba, 'rgba(25.0%, 50%, 100%, 0.5)')

        self.assertRaises(ValueError,
                          color_to_rgba, 'hsl(130, 30, 80%)')

        self.assertRaises(ValueError,
                          color_to_rgba, 'hsla(210., 90%, 70%, 0.5)')

if __name__ == '__main__':
    unittest.main()

