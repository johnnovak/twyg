import collections, math

try:
    import json                 # Python 2.6+
except ImportError:
    import simplejson as json   # Python 2.5 & Nodebox 1


def init(nodebox=False, ctx=None):
    if nodebox:
        # Simulate ximport
        import colors
        colors._ctx = ctx

        # "Injecting extra methods into the NodeBox Context object is
        # quite safe since the NodeBox 1 codebase is essentially frozen,
        # so the likelihood that future updates will break this is very
        # slim."
        #   -- Excerpt from Famous Last Words, vol 42.

        ctx.color = lambda r, g, b, a: colors.rgb(r, g, b, a)
        ctx.gradientfill = colors.gradientfill
        ctx.shadow = colors.shadow
        ctx.noshadow = colors.noshadow


def validate_margins(margins):
    calculate_margins(0, 0, margins)


def calculate_margins(width, height, margins):
    def is_percent(v):
        return v[-1] == '%'

    def percent_value(v):
        try:
            val = float(v[:-1])
        except ValueError:
            raise ValueError, 'Invalid percentage margin value: %s' % v
        if val < 0:
            raise (ValueError,
                   'Margin percentage value must be positive: %s' % v)
        elif val > 100:
            raise (ValueError,
                   'Margin percentage value must be less than 100: %s' % v)
        return val

    def value(v):
        try:
            val = float(v)
        except ValueError:
            raise ValueError, 'Invalid margin value: %s' % v
        if val < 0:
            raise ValueError, 'Margin value must be positive: %s' % v
        return val

    if len(margins) == 1:
        top = right = bottom = left = margins[0]

    elif len(margins) == 2:
        top = bottom = margins[0]
        right = left = margins[1]

    elif len(margins) == 4:
        top = margins[0]
        right = margins[1]
        bottom = margins[2]
        left = margins[3]
    else:
        raise ValueError, 'Invalid margin description: %s' % margins

    top_margin = (height * percent_value(top) / 100 if is_percent(top)
                  else value(top))

    right_margin = (width * percent_value(right) / 100 if is_percent(right)
                    else value(right))

    bottom_margin = (height * percent_value(bottom) / 100 if is_percent(bottom)
                     else value(bottom))

    left_margin = (width * percent_value(left) / 100 if is_percent(left)
                   else value(left))

    return top_margin, right_margin, bottom_margin, left_margin


def brightness(col):
    # Formula from:
    # http://www.nbdtech.com/Blog/archive/2008/04/27/Calculating-the-Perceived-Brightness-of-a-Color.aspx
    return math.sqrt(  .241 * pow(col.r, 2)
                     + .691 * pow(col.g, 2)
                     + .068 * pow(col.b, 2))


def loadjson(path):
    """ Loads a JSON file. """
    try:
        fp = file(path)
        data = json.load(fp)
        fp.close()
    except Exception, e:
        raise ValueError("Error loading JSON file '%s':\n\t%s" % (path, e))
    return data


###############################################################################

_textwidth_cache = collections.defaultdict(dict)

def textwidth(ctx, txt, fontname, fontsize):
    """
    Memoized textwidth() function.

    The width of a string returned by textwidth() equals the sum of the
    widths of its constituting characters, so only need to simply cache
    the widths of the individual characters.
    """

    key = fontname + str(fontsize)
    fs = _textwidth_cache[key]
    w = 0

    for c in txt:
        if c not in fs:
            fs[c] = ctx.textwidth(c)
        w += fs[c]

    return w


def createpath(ctx, segments, close=True):
    """ Create a path object from a list of segment definitions.

    Each element of the list ``segments`` defines a segment of the path.
    If the element is a single object, it defines an endpoint of a
    straight line. If the element is a 2 element list, it defines the
    two endpoints of a straight line in `[p0, p1]` format. If the
    element is a 4 element lists, it  defines a Bezier-path in `[p0, p1,
    p2, p3]` format, where `p0` and `p3` are the two endpoints and `p1`
    and `p2` the two control points. All points objects should have `x`
    and `y` properties. ``close`` controls whether the resulting path
    shall be automatically closed or not.
    """

    ctx.autoclosepath(close)

    s0 = segments[0]
    if type(s0) in (list, tuple):
        ctx.beginpath(s0[0].x, s0[0].y)
    else:
        ctx.beginpath(s0.x, s0.y)

    for s in segments:
        if type(s) in (list, tuple):
            if len(s) == 2:
                ctx.lineto(s[1].x, s[1].y)
            elif len(s) == 4:
                ctx.curveto(s[1].x, s[1].y, s[2].x, s[2].y, s[3].x, s[3].y)
            else:
                raise ValueError, 'Invalid path segment: %s' % s
        else:
            ctx.lineto(s.x, s.y)

    return ctx.endpath(draw=False)

