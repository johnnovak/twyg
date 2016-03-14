import os, shutil, sys, time


sys.path.append(os.path.join('..'))

from twyg.cairowrapper import Context, color


class DropShadowTest(object):
    def __init__(self, ctx):
        self.ctx = ctx
        self.w = 40
        self.h = 30
        self.ypad = 20
        self.xpad = 30
        self.xstart = 20
        self.ystart = 80
        self.dx = self.dy = 5

        self.shadowcolor = color(0, 0, 0, .4)
        self.fillcolor = color(.4, .8, .9)
        self.strokecolor = color(.2, .6, .7)

        # TODO
#        self.blur_list = [0.0, 1.0, 1.5, 3.0, 6.0]
#        self.dpi_list = [20, 40, 72, 150, 300, 600]
        self.blur_list = [0.0, 1.0, 1.5]
        self.dpi_list = [20, 40, 72, 150]
        self.title = ''

        self.path = ctx.rect(0, 0, self.w, self.h, roundness=.5, draw=False)

    def draw(self):
        self.drawlabels()
        self.drawtable()

    def drawlabels(self):
        c = self.ctx
        c.fill(.2)

        # Title
        c.fontsize(16)
        c.text(self.title, self.xstart, self.ystart - 45)

        # Blur labels
        c.fontsize(12)
        x = self.xstart
        y = self.ystart + 20
        for b in self.blur_list:
            c.text('r=' + str(b), x, y)
            y += self.h + self.ypad

        # DPI labels
        y = self.ystart - 15
        x = self.xstart + 50
        for d in self.dpi_list:
            c.text(str(d) + 'dpi', x, y)
            x += self.w + self.xpad

    def drawshape(self, x, y, blur):
        c = self.ctx
        c.shadow(dx=self.dx, dy=self.dy, blur=blur, clr=self.shadowcolor)
        c.push()
        c.translate(x, y)
        c.fill(self.fillcolor)
        c.stroke(self.strokecolor)

        t1 = time.clock()
        c.drawpath(self.path)
        t2 = time.clock()

        c.fontsize(7)
        c.fill(1)
        c.text('%.3gs' % (t2 - t1), 10, 17)
        c.pop()

    def drawtable(self):
        c = self.ctx
        x = self.xstart + 50
        for dpi in self.dpi_list:
            c._bitmap_dpi = dpi
            y = self.ystart
            for blur in self.blur_list:
                self.drawshape(x, y, blur)
                y += self.h + self.ypad
            x += self.w + self.xpad


def general_test(fname, fmt, scale):
    fname += '.' + fmt
    print "Writing '%s'" % fname

    ctx = Context()
    ctx.initsurface(200, 100, fmt, fname, scale)

    # Rect
    ctx.stroke(color(.7))
    ctx.strokewidth(1)
    ctx.fill(color(.9))
    ctx.rect(10, 10, 50, 50)

    # Line
    ctx.stroke(1, 0, 0, .2)
    ctx.strokewidth(3)
    ctx.line(30, 30, 150, 40)

    # Oval
    c = (1, .8, 0)
    ctx.stroke(*c)
    ctx.strokewidth(1)
    ctx.nofill()
    ctx.oval(130, 20, 40, 40)
    ctx.oval(130, 30, 40, 20)

    # Path - straight lines
    c = color(1, .5)
    ctx.fill(c)
    ctx.stroke(0, .3)
    ctx.strokewidth(.5)
    ctx.beginpath(40, 20)
    ctx.lineto(80, 30)
    ctx.lineto(60, 80)
    ctx.endpath()

    # Path - curves
    c = [0, .4]
    ctx.fill(*c)
    ctx.stroke(ctx.color(1, 0, 0))
    ctx.strokewidth(.5)
    ctx.beginpath(80, 40)
    ctx.curveto(100, 40, 100, 50, 100, 60)
    ctx.curveto(90, 50, 90, 60, 90, 90)
    ctx.endpath()

    # Text
    ctx.fill(.3)
    ctx.font('ITC Garamond Std Light', 12)
    ctx.text('NodeBox', 10, 80)

    ctx.fill((.5))
    ctx.fontsize(7)
    ctx.text('0123456789ABCDEFG', 10, 90)

    ctx.fill(0)
    ctx.text('EDGE', 0, 100)

    # Rect edge cases
    ctx.fill(1, 0, 0)
    ctx.stroke(0, 1, 0)
    ctx.rect(70, 5, 1, 1)       # should appear as a point
    ctx.stroke(0, 1, 0)
    ctx.rect(70, 10, 10, 0)     # should appear as a horiz line
    ctx.rect(85, 5, 0, 5)       # should appear as a vert line
    ctx.rect(90, 10, 0, 0)      # nothing should be drawn

    # Oval edge cases
    ctx.oval(100, 20, 10, 5)    # normal ellipse

    ctx.stroke(1, 0, 0)
    ctx.fill(0, 1, 0)
    ctx.oval(100, 20, -10, -5)  # should appear flipped (not supported)

    # Gradient test
    clr1 = ctx.color(0.5, 0.3, 0.4)
    clr2 = ctx.color(0.7, .95, 0.0)

    ctx.nostroke()
    ctx.fill(clr1)
    ctx.oval(100, 55, 9, 30)

    ctx.fill(clr2)
    ctx.oval(131, 55, 9, 30)

    #path = oval(110, 50, 20, 40, draw=False)
    w = 20.
    h = 40.
    path = ctx.rect(110, 50, w, h, draw=False)
    ctx.gradientfill(path, clr1, clr2, type='linear', dx=0, dy=0, spread=(h/w))

    # Rounded rects & transparent edge test
    ctx.fill(0.3, 0.6, 0.4)
    ctx.stroke(0, 0.2)
    ctx.strokewidth(1)
    ctx.rect(170, 50, 25, 15, roundness=0.4)

    ctx.nostroke()
    ctx.rect(170, 67, 25, 20, roundness=0.6)

    ctx.fill(0.5, 0.9, 0.8)
    ctx.stroke(1, .5, 0, 0.4)
    ctx.strokewidth(3)
    ctx.rect(155, 67, 10, 30, roundness=0.3)

    ctx.writesurface()


def color_test(fname, fmt, scale):
    fname += '.' + fmt
    print "Writing '%s'" % fname

    ctx = Context()
    ctx.initsurface(280, 100, fmt, fname, scale)

    side = 5
    offs = 5
    col1 = ctx.color(.1, .2, .15)
    col2 = ctx.color(.3, .6, .3)
    col3 = ctx.color(.3, .2, 0, .5)
    ctx.nostroke()
    ctx.scale(4)
    for i in range(10):
        ctx.fill(col1)
        ctx.rect(offs + side * i, offs, side, side)
        ctx.fill(col2)
        ctx.rect(offs + side * i, offs + side, side, side)
        ctx.fill(col3)
        ctx.rect(offs + side * i, offs + side * 2, side, side)
        col1 = col1.lighten(.1)
        col2 = col2.blend(color(1), .2)
        col3 = col3.lighten(.1)

    ctx.writesurface()


def dropshadow_test(fname, fmt, scale):
    fname += '.' + fmt
    print "Writing '%s'" % fname

    ctx = Context()
    ctx.initsurface(500, 1010, fmt, fname, scale)

    ctx._shadow_blur_passes = 1
    dst = DropShadowTest(ctx)
    dst.ystart = 80
    dst.title = '1 pass (box blur)'
    dst.draw()

    ctx._shadow_blur_passes = 2
    dst = DropShadowTest(ctx)
    dst.ystart = 410
    dst.title = '2 passes (triangle blur)'
    dst.draw()

    ctx._shadow_blur_passes = 3
    dst = DropShadowTest(ctx)
    dst.ystart = 740
    dst.title = '3 passes (bicubic blur)'
    dst.draw()

    ctx.writesurface()


if __name__ == '__main__':
    output_dpi = 300.0
    output_scale = 1.0
    scale = output_dpi / 72.0 * output_scale

    outpath = 'out'
    try:
        shutil.rmtree(outpath)
    except OSError:
        pass
    os.mkdir(outpath)

    fname = os.path.join(outpath, 'general-test')
    general_test(fname, 'pdf', scale)
    general_test(fname, 'svg', scale)
    general_test(fname, 'png', scale)

    fname = os.path.join(outpath, 'color-test')
    color_test(fname, 'pdf', scale)
    color_test(fname, 'svg', scale)
    color_test(fname, 'png', scale)

    fname = os.path.join(outpath, 'dropshadow-test')
    dropshadow_test(fname, 'pdf', scale)
    dropshadow_test(fname, 'svg', scale)
    dropshadow_test(fname, 'png', scale)

