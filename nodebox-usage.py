ximport('twyg')

datafile = 'example-data/data1.json'
configfile = 'configs/config9.yml'
colorschemefile = 'colors/colors6.yml'

tree = twyg.buildtree(datafile, configfile, colorschemefile)

width, height = tree.calclayout()

#padtop, padleft, padbottom, padright = twyg.calculate_margins(width, height, margins)
#width += padleft + padright
#height += padtop + padbottom
#tree.shiftnodes(padleft, padtop)

size(width, height)
background(*tree.background_color())

tree.draw()
