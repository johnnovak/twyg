ximport('twyg')

size(1000, 400)
background(1)

configfile = '/Users/jnovak/Work/Code/twyg/configs/boxes.twg'

tree = twyg.buildtree('fig-node-box1.json', configfile)
tree.calclayout()
tree.draw()


