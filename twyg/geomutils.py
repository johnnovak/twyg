import math

from twyg.geom import Vector2


def calc_regular_polygon_points(cx, cy, r, numsides, rotation=0):
    """ Calculates the vertices of a regular n-sided polygon. """

    points = []
    a = 2 * math.pi / numsides
    sa = math.radians(rotation)

    for i in range(numsides + 1):
        x = cx + r * math.cos(sa + a * i)
        y = cy - r * math.sin(sa + a * i)
        points.append(Vector2(x, y))

    return points


def calc_regular_polygon_intersections(w, ystep, **kwargs):
    h = w
    r =  w / 2.
    cx = r
    cy = r
    numsides = kwargs['numSides']
    rotation = kwargs['rotation']

    points = calc_regular_polygon_points(cx, cy, r, numsides, rotation)
    points = slice_shape(points, 0, h, ystep)

    return points, w, h


def calc_ellipse_intersections(w, ystep, **kwargs):
    aspectratio = kwargs['aspectRatio']
    maxwidth = kwargs['maxWidth']

    h = w / float(aspectratio)
    if ystep > h:
        s = 1 + ystep / h
        h *= s
        w *= s

    w = min(w, maxwidth)

    points = slice_ellipse(0, 0, w, h, ystep, rfactor=1.0)
    return points, w, h


def slice_shape(points, y, h, ystep):
    """
    Calculate the intersections of a convex shape and a set of
    equidistant horizontal lines.

    `points`
       points defining the shape segments
    `y`
       topmost (lowest value) y coordinate of the original shape
    `h`
       height of the original shape
    `ystep`
        vertical distance between horizontal lines

    Only point-pairs are returned, single-point intersections are
    omitted (e.g. when a horizontal line goes exactly through a single
    vertex).

    The point-pairs are returned in a 3-dimensional array:

        points = [[l1p1, l2p2], [l2p1, l2p2], ... [lnp1, lnp2]]

    The points have the following properties:

        lnp1.y  = lnp2.y
        lnp1.x <= lnp2.x
        lnpm.y  < l(n + 1)pm.y
    """
    # Close the shape if the shape is already closed that doesn't
    # affect the algorithm
    points.append(points[0])

    numlines = (int) (float(h) / ystep)

    # Special case when ystep > h / 2
    if numlines == 1:
        numlines = 2

    # Center lines to the vertical center of the shape
    y = y + (h - (numlines - 1) * ystep) / 2.

    # Iterate through all horizontal lines (starting from the lowest y
    # coordinate) and calculate the two intersection points of each line
    # with the shape segments (some lines may result in zero or one
    # intersections, these will be omitted).

    intersections = []

    for l in range(numlines):
        pointpair = []

        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]

            if p1.y > p2.y:
                p1, p2 = p2, p1

            if y >= p1.y and y < p2.y:
                # Special case for p1.x = p2.x (vertical line)
                dx = p2.x - p1.x + 1e-5

                # Calculate the intersection of a horizontal line and a
                # single shape segment
                dy = p2.y - p1.y
                m =  dy / dx
                x =  p1.x + 1 / m * (y - p1.y)

                pointpair.append(Vector2(x, y))

                # There should be two (or zero) intersections for each
                # horizontal line
                if len(pointpair) == 2:
                    if pointpair[0].x > pointpair[1].x:
                        pointpair[0], pointpair[1] = pointpair[1], pointpair[0]

                    intersections.append(pointpair)
                    break
        y += ystep

    return intersections


def slice_ellipse(x, y, w, h, ystep, rfactor=1.0):
    """
    Calculate the intersections of an ellipse (or two elliptical arcs
    horizontally symmetrical to the center point) and a set of
    equidistant horizontal lines.

    ``x, y, w, h``
        Bounding box of the ellipse.
    ``ystep``
        Vertical distance between horizontal lines.
    ``rfactor``
        If ``rfactor`` equals 1.0, a normal ellipse is used. If
        ``rfactor`` is greater than 1.0, two elliptical arcs
        horizontally symmetrical to the center point will be calculated
        (rfactor sets the 'flatness' of the arcs).

    The function returns the intersection point-pairs in the same format
    as ``slice_shape``.
    """

    if ystep >= h:
        return []

    points = []

    # Store original x center for the final mirroring step
    cxo = x + w / 2.

    # Calculate the "ovalness" of the ellipse and adjust center point
    xscale = float(w) / h
    x += h * xscale / 2.

    # If rfactor > 1, not a full half-arc will be used but only a
    # smaller symmetrical segment of it.  This is accomplished by
    # scaling the original radius up then adjusting the location of the
    # center point.
    r = h / 2.
    cx = x + r * (rfactor - 1)
    cy = y + r
    r *= rfactor

    # Special case when ystep > circle radius
    numlines = (int) (float(h) / ystep)
    if numlines == 1:
        numlines = 2

    # Adjust the x coords of the points so that the top and bottommost
    # points of the arc are always in the same position, regardless of
    # the rfactor
    xcorr = x - (cx - r * xscale) - w / 2.

    # Center points vertically
    py = y + (h - (numlines - 1) * ystep) / 2.

    while numlines:
        px = cx - math.sqrt(r * r - pow(py - cy, 2)) * xscale + xcorr
        points.append(Vector2(px, py))
        py += ystep
        numlines -= 1

    # Mirror points on the y axis and return point-pair arrays for each
    # line
    return [[p, Vector2(2 * cxo - p.x, p.y)] for p in points]


def arcpath(x, y, w, h, a1, da):
    #TODO insert formula reference 
    def _calc_arc_segment(cx, cy, x1, y1, x4, y4):
        ax = x1 - cx
        ay = y1 - cy
        bx = x4 - cx
        by = y4 - cy
        q1 = ax * ax + ay * ay
        q2 = q1 + ax * bx + ay * by

        d = ax * by - ay * bx
        if d == 0:
            d = 1e-15
        k2 = 1.3333333333 * (math.sqrt(2 * q1 * q2) - q2) / d

        x2 = cx + ax - k2 * ay
        y2 = cy + ay + k2 * ax
        x3 = cx + bx + k2 * by
        y3 = cy + by - k2 * bx

        return [Vector2(x1, y1), Vector2(x2, y2),
                Vector2(x3, y3), Vector2(x4, y4)]

    def _quad_startpoint(cx, cy, r, quad):
        """
        Quads:
        0: top right (0 - 90)
        1: top left (90 - 180)
        2: bottom left (180 - 270)
        3: bottom right (270 - 360)
        """
        quad %= 4
        if quad == 0:
            x1 = cx + r
            y1 = cy
        elif quad == 1:
            x1 = cx
            y1 = cy - r
        elif quad == 2:
            x1 = cx - r
            y1 = cy
        elif quad == 3:
            x1 = cx
            y1 = cy + r
        return [x1, y1]


    if da == 0 or w == 0 or h == 0:
        return []

    cx = x + w / 2.
    cy = y + h / 2.
    r = w / 2.

    a1 %= 360
    da = max(min(da, 360), -360)
    a2 = a1 + da

    quadstart =  (int) (math.floor(a1 / 90.))
    quadend = (int) (math.floor(a2 / 90.))

    a1 = math.radians(a1)
    a2 = math.radians(a2)

    a1x = cx + r * math.cos(a1)
    a1y = cy - r * math.sin(a1)
    a2x = cx + r * math.cos(a2)
    a2y = cy - r * math.sin(a2)

    points = []

    if quadstart == quadend:
        points.append(_calc_arc_segment(cx, cy, a1x, a1y, a2x, a2y))

    elif abs(quadstart - quadend) == 1:
        p = _quad_startpoint(cx, cy, r, quadend if da > 0 else quadstart)
        points.append(_calc_arc_segment(cx, cy, a1x, a1y, p[0], p[1]))
        points.append(_calc_arc_segment(cx, cy, p[0], p[1], a2x, a2y))

    else:
        if da > 0:
            quadstart += 1
            d = 1
        else:
            quadend += 1
            d = -1

        p = _quad_startpoint(cx, cy, r, quadstart)
        points.append(_calc_arc_segment(cx, cy, a1x, a1y, p[0], p[1]))

        quad = quadstart
        while quad != quadend:
            p1 = _quad_startpoint(cx, cy, r, quad)
            p2 = _quad_startpoint(cx, cy, r, quad + d)
            points.append(_calc_arc_segment(cx, cy, p1[0], p1[1],
                                                    p2[0], p2[1]))
            quad += d

        p = _quad_startpoint(cx, cy, r, quadend)
        points.append(_calc_arc_segment(cx, cy, p[0], p[1], a2x, a2y))

    return points


def halfcircle(cx, y1, y2, rfactor, dir, y):
    dir = -dir
    dy = float(y2 - y1)
    r = dy / 2
    cy = (y1 + y2) / 2.
    r *= rfactor
    xcorr = dir * math.sqrt(r * r - pow(y1 - cy, 2))
    return cx - dir * math.sqrt(r * r - pow(y - cy, 2)) + xcorr


def round_corner(p1, p2, p3, r):
    """ Calculate the Bezier-path segments defining a circular rounded
    corner of radius ``r`` of the two straight line segments `(p1,p2)`
    and `(p2,p3)`.

    Fit a circle of radius ``r`` into the triangle defined by points
    ``p1``, ``p2`` and ``p3`` so that segments `(p1,p2)` and `(p3,p2)`
    are tangents to the circle, then return the Bezier-path of the arc
    segment of radius ``r`` between points ``p1`` and ``p3``, facing
    ``p1``.
    """

    # Optimization for the 90 degree case when the two segments are
    # parallel to the axes (~2.3x speedup). This is used frequently for
    # drawing rounded rectangles.
    d = 1e-5
    s1_horiz = abs(p1.y - p2.y) < d
    s2_horiz = abs(p2.y - p3.y) < d
    s1_vert = abs(p1.x - p2.x) < d
    s2_vert = abs(p2.x - p3.x) < d

    # Handle 0, 180 degree and single point cases
    if (s1_horiz and s2_horiz) or (s1_vert and s2_vert):
        return []

    if (s1_vert and s2_horiz) or (s1_horiz or s2_vert):
        if s1_horiz:
            dx = p2.x > p1.x
            dy = p3.y > p2.y
        else:
            dx = p3.x > p2.x
            dy = p2.y > p1.y

        # the conditions calculating the arc's angles can be derived
        # from the following table:
        #
        #  dx   dy   sa   da s1_horiz quadrant
        # --- ---- ---- ---- -------- --------
        #   1    1   90  -90   1         1
        #   0    1    0  -90   0         4
        #   0    0  270  -90   1         3
        #   1    0  180  -90   0         2
        #   0    0    0   90   0         1
        #   1    0  270   90   1         4
        #   1    1  180   90   0         3
        #   0    1   90   90   1         2
        if (   (dx == dy) and s1_horiz
            or (dx != dy) and not s1_horiz):
            da = -90
        else:
            da = 90

        if s1_horiz:
            sa = 90 if dy else 270
        else:
            sa = 180 if dx else 0

        # Determine which quadrant should the arc be drawn in
        q = sa
        if da < 0:
            q -= 90
            if q < 0:
                q += 360

        r *= 2
        x = p2.x
        y = p2.y
        if q == 0:
            x -= r
        elif q == 180:
            y -= r
        elif q == 270:
            x -= r
            y -= r

        return arcpath(x, y, r, r, sa, da)

    # General case (we've already handles the 0 and 180 degree cases)
    a1 = (p1 - p2).a
    a2 = (p3 - p2).a
    ang = a2 - a1

    if ang > math.pi:
        ang -= 2 * math.pi
    elif ang < -math.pi:
        ang += 2 * math.pi

    # Length of the segment between p2 and the center of the circle
    aa = r / math.sin(ang / 2)

    # Calculate the center point of the circle
    c = Vector2(m=abs(aa), angle=a1 + ang / 2) + p2

    # Distance from p2 to the tangent points
    dd = r / math.tan(ang / 2)

    # Tangent point of segments p1, p2
    p = Vector2(m=abs(dd), angle=a1) + p2

    # Tangent point of segments p3, p2
    q = Vector2(m=abs(dd), angle=a2) + p2

    # Calculate a third point on the circle halfway between the two
    # tangent points. This will be on the arc segment that should be
    # drawn, which is needed to be able to determine the correct
    # direction of the arc.
    m = Vector2(m=abs(aa) - r, angle=a1 + ang / 2) + p2

    # Calculate the positions of points p, q and m on the circle
    # expressed as angles from the positive X axis.
    start_a = (p - c).a
    mid_a = (m - c).a
    end_a = (q - c).a

    # Start angle of the arc segment
    sa = start_a

    # Adjust arc length so the arc will always be drawn correctly in the
    # corner of the triangle.
    if start_a < mid_a < end_a or start_a > mid_a > end_a:
        da = end_a - start_a
    else:
        if start_a < end_a:
            da = -(start_a + 2 * math.pi - end_a)
        else:
            da = end_a + 2 * math.pi - start_a

    # Calculate Bezier points of the arc
    return arcpath(c.x - r, c.y - r, 2 * r, 2 * r,
                   math.degrees(sa), math.degrees(da))


def round_poly(points, r, close=True):
    """ Round a polygon defined by connecting segments by a specified
    radius.
    """

    # Handle degenerate cases
    if len(points) <= 1:
        return None
    if len(points) == 2:
        p0 = points[0]
        p1 = points[1]
        return [[p0, p1]]

    # Calculate corner arcs
    # TODO make a copy of points before appending
    arcs = []
    if close:
        points.append(points[0])
        points.append(points[1])

    for i in range(len(points) - 2):
        a = round_corner(points[i], points[i + 1], points[i + 2], r)
        if a:
            arcs.append(a)

    # Build full Bezier-path using the arcs and connect arc endpoints
    # with straight lines.
    if close:
        arcs.append(arcs[0])

    path = []
    if not close:
        p0 = points[0]
        p1 = arcs[0][0][0]
        path.append([p0, p1])

    for i in range(len(arcs) - 1):
        p0 = arcs[i][-1][-1]
        p1 = arcs[i + 1][0][0]
        path += arcs[i]
        path.append([p0, p1])

    path += arcs[-1]

    if not close:
        p0 = arcs[-1][-1][-1]
        p1 = points[-1]
        path.append([p0, p1])

    return path


def rounded_rect(x, y, w, h, r):
    points = [Vector2(x, y), Vector2(x + w, y),
              Vector2(x + w, y + h), Vector2(x, y + h)]

    return round_poly(points, r)


def intersect(p1, p2, p3, p4):
    c = (p1.x - p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x - p4.x)

    # The two lines are parallel
    if abs(c) < 1e-15:
        return None

    a = p1.x * p2.y - p1.y * p2.x
    b = p3.x * p4.y - p3.y * p4.x

    x = (a * (p3.x - p4.x) - (p1.x - p2.x) * b) / c
    y = (a * (p3.y - p4.y) - (p1.y - p2.y) * b) / c

    return Vector2(x, y)


def offset_poly(points, d, close=True):
    """ Offset polygon defined by ``points`` by amount ``d``.

    Works correctly only for small offsets and convex or "not too
    concave" polygons.
    """
    # Handle degenerate cases
    if len(points) <= 1:
        return points

    points.append(points[0])

    lines = []
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]

        # Calculate normal
        n = (p2 - p1).normalize().rotate(math.pi / 2)
        shift = n * d
        lines.append([p1 + shift, p2 + shift])

    points.pop()
    lines.append(lines[0])

    offs = []
    for i in range(len(lines) - 1):
        l1 = lines[i]
        l2 = lines[i + 1]
        offs.append(intersect(l1[0], l1[1], l2[0], l2[1]))

    offs.insert(0, offs.pop())
    return offs

