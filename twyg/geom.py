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

    def __repr__(self):
        return '(x=%s, y=%s, w=%s, h=%s)' % (self.x, self.y, self.w, self.h)

    def params(self):
        return self.x, self.y, self.w, self.h

    def points(self):
        return [Point2D(self.x,          self.y),
                Point2D(self.x + self.w, self.y),
                Point2D(self.x + self.w, self.y + self.h),
                Point2D(self.x,          self.y + self.h)]

    def expand(self, rect):
        r1x1 = self.x
        r1y1 = self.y
        r1x2 = r1x1 + self.w
        r1y2 = r1y1 + self.h

        r2x1 = rect.x
        r2y1 = rect.y
        r2x2 = r2x1 + rect.w
        r2y2 = r2y1 + rect.h

        x1 = min(r1x1, r2x1)
        y1 = min(r1y1, r2y1)
        x2 = max(r1x2, r2x2)
        y2 = max(r1y2, r2y2)

        self.x = x1
        self.y = y1
        self.w = x2 - x1
        self.h = y2 - y1

