ximport('twyg')

datafile = '/Users/jnovak/Work/Code/twyg/example-data/synthesis.json'
config = 'hive'
colorscheme = 'orbit'
margins = ['10%', '5%']

twyg.generate_output_nodebox(datafile, config, colorscheme=colorscheme, margins=margins)
