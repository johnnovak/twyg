import os, sys

from fig import *
from twyg.cairowrapper import context as ctx


init_surface(586, 270, scale=0.8)
ctx.background(ctx.color(1))

w = 80
h = 50
padx = 0
pady = 0

xo = 160
yo = 45

x = xo
y = yo

f = .2

col1 = ctx.color(.5, .2, .0)
col2 = ctx.color(.8, 1, .6)
textcol = ctx.color(.3)


ctx.font('Open Sans')
ctx.fontsize(18)

ctx.fill(textcol)
ctx.text('lighten', 85, y + 36)

ctx.text('0.2', x + w     + 26, y - 12)
ctx.text('0.4', x + w * 2 + 26, y - 12)
ctx.text('0.6', x + w * 3 + 26, y - 12)
ctx.text('0.8', x + w * 4 + 26, y - 12)

c = col1
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.lighten(f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.lighten(f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.lighten(f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.lighten(f)
ctx.fill(c)
ctx.rect(x, y, w, h)



white = ctx.color(1)

y += h + pady
x = xo
c = col1

ctx.fill(textcol)
ctx.text('blend to white', 20, y + 36)

ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.blend(white, f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.blend(white, f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.blend(white, f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.blend(white, f)
ctx.fill(c)
ctx.rect(x, y, w, h)



y += h + pady
x = xo

ctx.fill(textcol)
ctx.text('darken', 84, y + 36)

c = col2
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.darken(f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.darken(f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.darken(f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.darken(f)
ctx.fill(c)
ctx.rect(x, y, w, h)



black = ctx.color(0)

y += h + pady
x = xo

ctx.fill(textcol)
ctx.text('blend to black', 24, y + 36)

c = col2
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.blend(black, f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.blend(black, f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.blend(black, f)
ctx.fill(c)
ctx.rect(x, y, w, h)

x += w + padx
c = c.blend(black, f)
ctx.fill(c)
ctx.rect(x, y, w, h)


ctx.writesurface()

