import re
import sys

infile = sys.argv[1]
for line in file(infile):
    m = re.match('(.*)\[(.*)\],?', line)
    if not m:
        print line,
    else:
        pre, color = m.groups()
        r, g, b, a = color.split(',')
        r = float(r) * 255
        g = float(g) * 255
        b = float(b) * 255
#        print '%srgba(%3.0f, %3.0f, %3.0f, %1.3f),' % (pre, r, g, b, float(a))
        print '%s%02x%02x%02x,' % (pre, r, g, b)


