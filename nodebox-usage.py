ximport('twyg')

datafile = 'examples/data/data8.json'
configfile = 'configs/config14.twg'
colorschemefile = 'colors/turquise.twg'

tree = twyg.buildtree(datafile, configfile, colorschemefile)

width, height = tree.calclayout()

#padtop, padleft, padbottom, padright = twyg.calculate_margins(width, height, margins)
#width += padleft + padright
#height += padtop + padbottom
#tree.shiftnodes(padleft, padtop)

size(width, height)
background(tree.background_color())

tree.draw()
