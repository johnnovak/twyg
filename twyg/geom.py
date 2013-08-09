import math


class Vector2(object):
    """ Class representing two-dimensional vectors.

    The coordinate system used has the following properties:
        - the origo (0,0) is located in the top left corner
        - the positive x direction is from left to right
        - the positive y direction is from top to bottom
        - positive rotation is counter-clockwise
    """
    def __init__(self, *args, **kwargs):
        if args:
            if isinstance(args[0], Vector2):
                self.x = float(args[0].x)
                self.y = float(args[0].y)
                return
            elif len(args) < 2:
                raise ValueError, "Must specify 'x' and 'y' of new vector"
            self.x = float(args[0])
            self.y = float(args[1])
        else:
            if not ('m' in kwargs and 'angle' in kwargs):
                raise ValueError, "Must specify 'm' and 'angle' of new vector"
            m = kwargs['m']
            a = -kwargs['angle']
            self.x = m * math.cos(a)
            self.y = m * math.sin(a)

    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    m = property(magnitude)

    def angle(self):
        a = -math.atan2(self.y, self.x)
        if a < 0:
            a += math.pi * 2
        return a

    a = property(angle)

    def normalize(self):
        m = self.magnitude()
        if m != 0:
            self.x /= m
            self.y /= m
        return self

    def rotate(self, angle):
        angle = -angle
        cos = math.cos(angle)
        sin = math.sin(angle)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        self.x = x
        self.y = y
        return self

    def __add__(self, s):
        return Vector2(self.x + s.x, self.y + s.y)

    def __iadd__(self, s):
        self.x += s.x
        self.y += s.y
        return self

    def __sub__(self, s):
        return Vector2(self.x - s.x, self.y - s.y)

    def __isub__(self, s):
        self.x -= s.x
        self.y -= s.y
        return self

    def __mul__(self, s):
        return Vector2(self.x * s, self.y * s)

    def __rmul__(self, s):
        return Vector2(self.x * s, self.y * s)

    def __imul__(self, s):
        self.x *= s
        self.y *= s
        return self

    def __div__(self, s):
        return Vector2(self.x / s, self.y / s)

    def __idiv__(self, s):
        self.x /= s
        self.y /= s
        return self


class Rectangle(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def params(self):
        return self.x, self.y, self.w, self.h

    def points(self):
        return [Point2D(self.x,          self.y),
                Point2D(self.x + self.w, self.y),
                Point2D(self.x + self.w, self.y + self.h),
                Point2D(self.x,          self.y + self.h)]

