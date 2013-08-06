ximport('twyg')

datafile = 'examples/data/data2.json'
configfile = 'configs/config6.twg'
colorschemefile = 'colors/honey.twg'

tree = twyg.buildtree(datafile, configfile, colorschemefile)

width, height = tree.calclayout()

#padtop, padleft, padbottom, padright = twyg.calculate_margins(width, height, margins)
#width += padleft + padright
#height += padtop + padbottom
#tree.shiftnodes(padleft, padtop)

size(width, height)
background(tree.background_color())

tree.draw()
