#!/usr/bin/python

from gimpfu import *
import math
from collections import namedtuple 



def Combine_Layers_To_Sheet(IMAGE, DRAWABLE):

    height = 0
    width = 0
    imgHeight = 0
    imgWidth = 0
    maxWidth = 1920
    maxHeight = 1080

    # just packs via best fit - tries to make a square
    img = gimp.image_list()[0]

    # assumes all layers are meant to be drawn in same width/height as image size
    imgHeight = img.height
    imgWidth = img.width

    layers = pdb.gimp_image_get_layers(img)
    layerCount = Size(layers)

    if layerCount%2 == 0:
        rows = layerCount/2     # as int!
    else:
        rows = (layerCount-1)/2

    # add new layer to draw on
    combinedLayer=gimp.Layer(img,"Sprite Sheet",rows,rows,RGB_IMAGE,100,NORMAL_MODE)    # always square so cols = rows
    img.add_layer(combinedLayer,0)

    countPerRow = math.ceil(layerCount/rows)
    curCount = 0
    # create new layer that is the right size
    for layer in pdb.gimp_image_get_layers(img):
        height += layer.height
        width += layer.width
		# keep running total of lengths and widths for final size of new layer
		# max size of 1920x1080

    CombinedLayer = gimp.Layer(img,"SpriteSheet",cols,rows,RGB_IMAGE,100,NORMAL_MODE)

    display=pdb.gimp_display_new(img)

end


register(
	"Sprite Sheet",
	"Combine all layers into sprite sheet - assumes all layers are the same size",
	"Combine all layers into sprite sheet - assumes all layers are the same size and attempts a square sheet",
	"Brody Clark",
	"Brody Clark",
	"2022-2023",
	"<Image>/Tools",
	"RGB*, GRAY*",
	[   
        #(PF_INT, "Rows", "# of Rows", 1)
    ],
	[],

	Combine_Layer_To_Sheet)

main()