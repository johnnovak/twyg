import re, colorsys


# SVG 1.0 color keyword names
# ---------------------------
# Adapted from http://en.wikipedia.org/wiki/Web_colors#X11_color_names
# See also http://www.w3.org/TR/SVG/types.html#ColorKeywords

colornames = {
    # Pink colors
    'pink':                 (255, 192, 203),
    'lightpink':            (255, 182, 193),
    'hotpink':              (255, 105, 180),
    'deeppink':             (255,  20, 147),
    'palevioletred':        (219, 112, 147),
    'mediumvioletred':      (199,  21, 133),

    # Red colors
    'lightsalmon':          (255, 160, 122),
    'salmon':               (250, 128, 114),
    'darksalmon':           (233, 150, 122),
    'lightcoral':           (240, 128, 128),
    'indianred':            (205,  92,  92),
    'crimson':              (220,  20,  60),
    'firebrick':            (178,  34,  34),
    'darkred':              (139,   0,   0),
    'red':                  (255,   0,   0),

    # Orange colors
    'orangered':            (255,  69,   0),
    'tomato':               (255,  99,  71),
    'coral':                (255, 127,  80),
    'darkorange':           (255, 140,   0),
    'orange':               (255, 165,   0),
    'gold':                 (255, 215,   0),

    # Yellow colors
    'yellow':               (255, 255,   0),
    'lightyellow':          (255, 255, 224),
    'lemonchiffon':         (255, 250, 205),
    'lightgoldenrodyellow': (250, 250, 210),
    'papayawhip':           (255, 239, 213),
    'moccasin':             (255, 228, 181),
    'peachpuff':            (255, 218, 185),
    'palegoldenrod':        (238, 232, 170),
    'khaki':                (240, 230, 140),
    'darkkhaki':            (189, 183, 107),

    # Brown colors
    'cornsilk':             (255, 248, 220),
    'blanchedalmond':       (255, 235, 205),
    'bisque':               (255, 228, 196),
    'navajowhite':          (255, 222, 173),
    'wheat':                (245, 222, 179),
    'burlywood':            (222, 184, 135),
    'tan':                  (210, 180, 140),
    'rosybrown':            (188, 143, 143),
    'sandybrown':           (244, 164,  96),
    'goldenrod':            (218, 165,  32),
    'darkgoldenrod':        (184, 134,  11),
    'peru':                 (205, 133,  63),
    'chocolate':            (210, 105,  30),
    'saddlebrown':          (139,  69,  19),
    'sienna':               (160,  82,  45),
    'brown':                (165,  42,  42),
    'maroon':               (128,   0,   0),

    # Green colors
    'darkolivegreen':       ( 85, 107,  47),
    'olive':                (128, 128,   0),
    'olivedrab':            (107, 142,  35),
    'yellowgreen':          (154, 205,  50),
    'limegreen':            ( 50, 205,  50),
    'lime':                 (  0, 255,   0),
    'lawngreen':            (124, 252,   0),
    'chartreuse':           (127, 255,   0),
    'greenyellow':          (173, 255,  47),
    'springgreen':          (  0, 255, 127),
    'mediumspringgreen':    (  0, 250, 154),
    'lightgreen':           (144, 238, 144),
    'palegreen':            (152, 251, 152),
    'darkseagreen':         (143, 188, 143),
    'mediumseagreen':       ( 60, 179, 113),
    'seagreen':             ( 46, 139,  87),
    'forestgreen':          ( 34, 139,  34),
    'green':                (  0, 128,   0),
    'darkgreen':            (  0, 100,   0),

    # Cyan colors
    'mediumaquamarine':     (102, 205, 170),
    'aqua':                 (  0, 255, 255),
    'cyan':                 (  0, 255, 255),
    'lightcyan':            (224, 255, 255),
    'paleturquoise':        (175, 238, 238),
    'aquamarine':           (127, 255, 212),
    'turquoise':            ( 64, 224, 208),
    'mediumturquoise':      ( 72, 209, 204),
    'darkturquoise':        (  0, 206, 209),
    'lightseagreen':        ( 32, 178, 170),
    'cadetblue':            ( 95, 158, 160),
    'darkcyan':             (  0, 139, 139),
    'teal':                 (  0, 128, 128),

    # Blue colors
    'lightsteelblue':       (176, 196, 222),
    'powderblue':           (176, 224, 230),
    'lightblue':            (173, 216, 230),
    'skyblue':              (135, 206, 235),
    'lightskyblue':         (135, 206, 250),
    'deepskyblue':          (  0, 191, 255),
    'dodgerblue':           ( 30, 144, 255),
    'cornflowerblue':       (100, 149, 237),
    'steelblue':            ( 70, 130, 180),
    'royalblue':            ( 65, 105, 225),
    'blue':                 (  0,   0, 255),
    'mediumblue':           (  0,   0, 205),
    'darkblue':             (  0,   0, 139),
    'navy':                 (  0,   0, 128),
    'midnightblue':         ( 25,  25, 112),

    # Purple colors
    'lavender':             (230, 230, 250),
    'thistle':              (216, 191, 216),
    'plum':                 (221, 160, 221),
    'violet':               (238, 130, 238),
    'orchid':               (218, 112, 214),
    'fuchsia':              (255,   0, 255),
    'magenta':              (255,   0, 255),
    'mediumorchid':         (186,  85, 211),
    'mediumpurple':         (147, 112, 219),
    'blueviolet':           (138,  43, 226),
    'darkviolet':           (148,   0, 211),
    'darkorchid':           (153,  50, 204),
    'darkmagenta':          (139,   0, 139),
    'purple':               (128,   0, 128),
    'indigo':               ( 75,   0, 130),
    'darkslateblue':        ( 72,  61, 139),
    'slateblue':            (106,  90, 205),
    'mediumslateblue':      (123, 104, 238),

    # White/Gray/Black colors
    'white':                (255, 255, 255),
    'snow':                 (255, 250, 250),
    'honeydew':             (240, 255, 240),
    'mintcream':            (245, 255, 250),
    'azure':                (240, 255, 255),
    'aliceblue':            (240, 248, 255),
    'ghostwhite':           (248, 248, 255),
    'whitesmoke':           (245, 245, 245),
    'seashell':             (255, 245, 238),
    'beige':                (245, 245, 220),
    'oldlace':              (253, 245, 230),
    'floralwhite':          (255, 250, 240),
    'ivory':                (255, 255, 240),
    'antiquewhite':         (250, 235, 215),
    'linen':                (250, 240, 230),
    'lavenderblush':        (255, 240, 245),
    'mistyrose':            (255, 228, 225),
    'gainsboro':            (220, 220, 220),
    'lightgray':            (211, 211, 211),
    'silver':               (192, 192, 192),
    'darkgray':             (169, 169, 169),
    'gray':                 (128, 128, 128),
    'dimgray':              (105, 105, 105),
    'lightslategray':       (119, 136, 153),
    'slategray':            (112, 128, 144),
    'darkslategray':        ( 47,  79,  79),
    'black':                (  0,   0,   0)
}


# Precompile regular expressions for rgb(a) & hsl(a) format matching
i = '\s*([-+]?\d+)\s*'       # int
p = '\s*([-+]?\d+)\%\s*'     # percent
f = '\s*([-+]?\d*\.?\d+)\s*' # float

_re_rgb    = re.compile('rgb\(%s,%s,%s\)'     % (i, i, i))
_re_rgb_p  = re.compile('rgb\(%s,%s,%s\)'     % (p, p, p))
_re_rgba   = re.compile('rgba\(%s,%s,%s,%s\)' % (i, i, i, f))
_re_rgba_p = re.compile('rgba\(%s,%s,%s,%s\)' % (p, p, p, f))
_re_hsl    = re.compile('hsl\(%s,%s,%s\)'     % (i, p, p))
_re_hsla   = re.compile('hsla\(%s,%s,%s,%s\)' % (i, p, p, f))

del i, p, f


def _parse_hex(col):
    if len(col) == 0:
        raise ValueError
    if col[0] == '#':
        col = col[1:]

    if len(col) == 3:
        r = int(col[0], 16) / 15.
        g = int(col[1], 16) / 15.
        b = int(col[2], 16) / 15.
        return r, g, b

    elif len(col) == 6:
        r = int(col[0:2], 16) / 255.
        g = int(col[2:4], 16) / 255.
        b = int(col[4:6], 16) / 255.
        return r, g, b
    else:
        raise ValueError


def _conv_rgb(c):
    return min(max(0, float(c)), 255) / 255.


def _conv_percent(p):
    return min(max(0, float(p)), 100) / 100.


def _conv_alpha(a):
    return min(max(0, float(a)), 1)


def _conv_hue(h):
    return float(h) / 360


def color_to_rgba(col):
    # Convert to string to handle hex colors consisting of decimal
    # digits only correctly
    col = str(col).strip()
    a = 1.0

    if col in colornames:
        r, g, b = colornames[col]
        return r / 255., g / 255., b / 255., a

    try:
        r, g, b = _parse_hex(col)
        return r, g, b, a
    except ValueError:
        pass

    # rgb(r, g, b)
    m = _re_rgb.match(col)
    if m:
        r, g, b =  m.groups()
        r = _conv_rgb(r)
        g = _conv_rgb(g)
        b = _conv_rgb(b)
        return r, g, b, a

    # rgb(r%, g%, b%)
    m = _re_rgb_p.match(col)
    if m:
        r, g, b =  m.groups()
        r = _conv_percent(r)
        g = _conv_percent(g)
        b = _conv_percent(b)
        return r, g, b, a

    # rgba(r, g, b, a)
    m = _re_rgba.match(col)
    if m:
        r, g, b, a =  m.groups()
        r = _conv_rgb(r)
        g = _conv_rgb(g)
        b = _conv_rgb(b)
        a = _conv_alpha(a)
        return r, g, b, a

    # rgba(r%, g%, b%, a)
    m = _re_rgba_p.match(col)
    if m:
        r, g, b, a =  m.groups()
        r = _conv_percent(r)
        g = _conv_percent(g)
        b = _conv_percent(b)
        a = _conv_alpha(a)
        return r, g, b, a

    # hsl(h, s, l)
    m = _re_hsl.match(col)
    if m:
        h, s, l =  m.groups()
        h = _conv_hue(h)
        s = _conv_percent(s)
        l = _conv_percent(l)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return r, g, b, a

    # hsla(h, s, l, a)
    m = _re_hsla.match(col)
    if m:
        h, s, l, a =  m.groups()
        h = _conv_hue(h)
        s = _conv_percent(s)
        l = _conv_percent(l)
        a = _conv_alpha(a)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return r, g, b, a

    raise ValueError, ('Invalid color: %s' % col)


def rgba_to_color(r, g, b, a, format='rgba'):
    r = min(max(r, 0), 1)
    g = min(max(g, 0), 1)
    b = min(max(b, 0), 1)
    a = min(max(a, 0), 1)

    if format == 'hex':
        return '#%02x%02x%02x' % (r * 255 + .5, g * 255 + .5, b * 255 + .5)

    if format == 'rgb':
        return 'rgb(%.0f, %.0f, %.0f)' % (r * 255, g * 255, b * 255)

    if format == 'rgba':
        return 'rgba(%.0f, %.0f, %.0f, %.3f)' % (r * 255, g * 255, b * 255, a)

    if format == 'rgb_p':
        return 'rgb(%.0f%%, %.0f%%, %.0f%%)' % (r * 100, g * 100, b * 100)

    if format == 'rgba_p':
        return ('rgba(%.0f%%, %.0f%%, %.0f%%, %.3f)'
                % (r * 100, g * 100, b * 100, a))

    if format == 'hsl':
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return 'hsl(%.0f, %.0f%%, %.0f%%)' % (h * 360, s * 100, l * 100)

    if format == 'hsla':
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return ('hsla(%.0f, %.0f%%, %.0f%%, %.3f)'
                % (h * 360, s * 100, l * 100, a))

    raise ValueError, 'Invalid color format: %s' % format

