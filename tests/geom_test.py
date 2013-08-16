import math, os, sys, unittest


sys.path.append(os.path.join('..'))

from twyg.geom import Vector2


deg = math.degrees
rad = math.radians


class TestEvalExpr(unittest.TestCase):

    def assert_equals(self, a, b):
        self.assertTrue(abs(a - b) < 1e-12)

    def test_constructor_cartesian1(self):
        v = Vector2(3, -4)
        self.assert_equals(5, v.m)
        self.assert_equals(53.13010235415598, deg(v.a))

    def test_constructor_cartesian2(self):
        v = Vector2(4, -4)
        self.assert_equals(5.6568542494923806, v.m)
        self.assert_equals(45.0, deg(v.a))

    def test_normalize(self):
        v = Vector2(4, -4)
        self.assert_equals(5.65685424949238, v.m)
        self.assert_equals(45.0, deg(v.a))
        v.normalize()
        self.assert_equals(1.0, v.m)
        self.assert_equals(45.0, deg(v.a))

    def test_rotate_positive(self):
        v = Vector2(4, -4)
        v.rotate(rad(-15))
        self.assert_equals(30.0, deg(v.a))

    def test_rotate_negative(self):
        v = Vector2(4, -4)
        v.rotate(rad(30))
        self.assert_equals(75.0, deg(v.a))

    def test_constructor_polar(self):
        v = Vector2(angle=rad(30), m=1)
        self.assert_equals(30.0, deg(v.a))
        self.assert_equals(1.0, v.m)
        self.assert_equals(0.86602540378443, v.x)
        self.assert_equals(-0.5, v.y)

    def test_constructor_copy(self):
        v1 = Vector2(angle=rad(30), m=1)
        v2 = Vector2(v1)
        self.assert_equals(v2.x, v1.x)
        self.assert_equals(v2.y, v1.y)
        self.assert_equals(v2.m, v1.m)
        self.assert_equals(v2.a, v1.a)

    def test_scalar_multiply_right(self):
        v = Vector2(3, 2)
        m, a = v.m, v.a
        v = v * 2
        self.assert_equals(a, v.a)
        self.assert_equals(m * 2, v.m)

    def test_scalar_multiply_left(self):
        v = Vector2(3, 2)
        m, a = v.m, v.a
        v = 2 * v
        self.assert_equals(a, v.a)
        self.assert_equals(m * 2, v.m)

    def test_scalar_multiply_and_assign(self):
        v = Vector2(3, 2)
        m, a = v.m, v.a
        v *= 2
        self.assert_equals(a, v.a)
        self.assert_equals(m * 2, v.m)

    def test_scalar_divide_and_assign(self):
        v = Vector2(3, 2)
        m, a = v.m, v.a
        v /= 2
        self.assert_equals(a, v.a)
        self.assert_equals(m / 2, v.m)

    def test_scalar_divide_right(self):
        v = Vector2(3, 2)
        m, a = v.m, v.a
        v = v / 2
        self.assert_equals(a, v.a)
        self.assert_equals(m / 2, v.m)


if __name__ == '__main__':
    unittest.main()

