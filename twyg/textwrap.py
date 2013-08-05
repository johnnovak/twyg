from twyg.hyphenator import hyphenate_word
from twyg.geom import Rectangle


_hyphenate_word_cache = {}


def _calc_inside_rects(points):
    """
    Calculate a list of horizontal rectangles fitting into a convex
    shape.

    ``points``
        A list of intersection point-pairs of a set of equidistant
        horizontal lines intersecting the segments defining shape
        (should be calculated by ``slice_shape``).

    Rectangles are returned as a list of ``[x, y, width, height]``
    arrays.
    """
    rects = []
    for i in range(len(points) - 1):
        p11, p12 = points[i]
        p21, p22 = points[i + 1]

        x = max(p11.x, p21.x)
        y = p11.y
        w = min(p12.x, p22.x) - x
        h = p21.y - p11.y

        rects.append(Rectangle(x, y, w, h))

    return rects


def _hyphenate_word(word):
    """ Memoized hyphenate_word() function. """
    cache = _hyphenate_word_cache
    if word not in cache:
        cache[word] = hyphenate_word(word)
    return cache[word][:]


def _splittext(txt, textwidth_func):
    words = txt.split()
    wordwidths = [textwidth_func(w) for w in words]
    spacewidth = textwidth_func(' ')
    return words, wordwidths, spacewidth


def _wraptext(words, wordwidths, spacewidth, textwidth_func, rects=None,
              maxwidth=0, hyphenate=False, max_spacewidth_factor=5):
    """
    Wrap text in a list of variable-width or fixed-width lines.

    ``words`` should contain the text as a list of words, ``wordwidths``
    the width of each word from the words list and ``spacewidth`` the
    width of a single space character. The function returns a list of
    strings containing the text in each line and a list of line widths.

    TODO max_spacewidth_factor, hyphenate

    In variable-width mode, ``rects`` holds a list of Rectangle objects
    that represent the blank lines the text should be wrapped into. The
    value of ``maxwidth`` is disregarded in this case. The following
    three outcomes are possible:

        len(lines) = len(rects)   -- optimal wrap
        len(lines) > len(rects)   -- can't fit text into the available
                                     rects
        len(lines) < len(rects)   -- suboptimal wrap

    In fixed-width mode, ``rects`` is None and ``maxwidth`` holds the
    fixed line length (must be greater than zero).
    """

    if not rects and maxwidth <= 0:
        raise (ValueError,
               'maxwidth must be greater than 0 if no rects are provided')

    maxwidth = max(maxwidth, max(wordwidths))

    lines = ['']         # wrapped text per each line
    linewidths = [0]     # linewidth of each line (including spaces)

    currline = currword = linewidth = 0
    maxlinewidth = rects[currline].w if rects else maxwidth

    if hyphenate:
        words = words[:]
        wordwidths = wordwidths[:]

    while currword < len(words):
        word = words[currword]

        # Start a new line if word doesn't fit into the current line
        if (linewidth
            + (spacewidth if linewidth > 0 else 0)
            + wordwidths[currword] > maxlinewidth):

            # Special path if hyphenation is enabled and there's enough
            # white space in the line
            if (hyphenate and maxlinewidth - linewidth
                > spacewidth * max_spacewidth_factor):

                parts = _hyphenate_word(word)
                parts[0] = ' ' + parts[0]
                partial_word = ''

                # Try to jam in as many syllables from the word at the
                # end of the line as possible
                for i, p in enumerate(parts):
                    partwidth = textwidth_func(p + '-')
                    if linewidth + partwidth <= maxlinewidth:
                        partial_word += p
                        linewidth += partwidth
                    else:
                        break

                if partial_word:
                    # Remove initial space if we're at the start of a
                    # line
                    if not lines[currline]:
                        partial_word = partial_word[1:]
                        linewidth -= spacewidth

                    # Add partial word to the end of the line
                    lines[currline] += partial_word + '-'
                    linewidths[currline] = linewidth
                    currword += 1

                    # Insert remaining parts before the next word as a
                    # "new word"
                    remaining_parts = ''.join(parts[i:])
                    words.insert(currword, remaining_parts)
                    wordwidths.insert(currword,
                                      textwidth_func(words[currword]))

            # Move to the next line
            currline += 1
            lines.append('')
            linewidths.append(0)

            # Stop if all the words don't fit into the number of
            # available rects (note: there's an extra blank line now at
            # the end of lines that ensures that len(lines) > len(rects))
            if rects and currline >= len(rects):
                break

            maxlinewidth = rects[currline].w if rects else maxwidth
            linewidth = 0

            # The widths need to be checked again because it's not
            # guaranteed that the word will fit into the next blank line
            continue

        # Append spaces between words after the first word on the line
        if lines[currline]:
            lines[currline] += ' '
            linewidth += spacewidth

        # Append word and update state variables
        lines[currline] += words[currword]
        linewidth += wordwidths[currword]
        linewidths[currline] = linewidth
        currword += 1

    return lines, linewidths


def wrap_rect(txt, lineheight, textwidth_func, maxwidth,
              hyphenate=False, hyphen_min_words=10):

    # Calculate word widths & space width
    words, wordwidths, spacewidth = _splittext(txt, textwidth_func)

    hyphenate &= len(words) > hyphen_min_words

    lines, linewidths = _wraptext(words, wordwidths, spacewidth,
                                  textwidth_func, maxwidth=maxwidth,
                                  hyphenate=hyphenate)
    numlines = len(lines)
    if numlines == 1:
        w = linewidths[0]
        h = lineheight
        rects = [Rectangle(0, 0, w, lineheight)]
    else:
        w = maxwidth
        h = lineheight * numlines
        rects = ([Rectangle(0, i * lineheight, w, lineheight)
                 for i in range(numlines)])

    return lines, linewidths, rects, w, h


def wrap_shape(txt, lineheight, textwidth_func, shapefunc,
               hyphenate=False, hyphen_min_words=10, **kwargs):

    # Initial shape width & height

    # Must be >= lineheight
    base_width = lineheight * 4
    scalefactor = 0.5
    currscale = 1.0
    params = []
    lastiteration = False
    null_result = [[], [], [], 0.0, 0.0]

    # Calculate word widths & space width
    words, wordwidths, spacewidth = _splittext(txt, textwidth_func)
    hyphenate &= len(words) > hyphen_min_words

    while 1:
        w = base_width * currscale

        points, w, h = shapefunc(w, lineheight, **kwargs)
        if not points:
            return null_result

        rects = _calc_inside_rects(points)

        lines, linewidths = _wraptext(words, wordwidths, spacewidth,
                                      textwidth_func, rects=rects,
                                      hyphenate=hyphenate)
        if lastiteration:
            break

        numlines = len(lines)
        numrects = len(rects)

        params.append({
            'numlines': numlines,
            'numrects': numrects,
            'currscale': currscale
        });

        # Optimal solution found: all rects are filled with text.
        if numlines == numrects:
            break

        # Otherwise try to iteratively "zoom-in" on the optimal
        # solution: halve step size and change scale direction in case
        # of over or undershoot.
        if (numlines < numrects and scalefactor > 0 or
            numlines > numrects and scalefactor < 0):

            scalefactor *= -.5

        # If no optimal solution was found in 20 iterations, simply pick
        # the best solution or return empty values if no solution was
        # found
        if len(params) >= 20:
            params = [p for p in params if p['numrects'] > p['numlines']]
            if not params:
                return null_result

            params = sorted(params,
                            key=lambda p: p['numrects'] - p['numlines'])

            currscale = params[0]['currscale']
            lastiteration = True
            continue

        currscale *= 1 + scalefactor

    return lines, linewidths, rects, w, h

