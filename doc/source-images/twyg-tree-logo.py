# twyg tree logo
# --------------
# Requires NodeBox1 (http://nodebox.net/code/index.php/Home)
# and the L-system library (http://nodebox.net/code/index.php/L-system)

background(None)
size(590, 430)

lsystem = ximport("lsystem")

stroke(0.122, 0.545, 0.553, 1)

def segment(length, generations, time, id):
  if generations > 0:
    strokewidth(generations ** 2.1)
      line(0, 0, 0, -length)

tree = lsystem.strong()
tree.segment = segment
tree.draw(290, 390, 6)

