#!/usr/bin/env python

from gimpfu import *
import math
from array import array


def Combine_Layers_To_Sheet():

    MAX_WIDTH   = 1920
    MAX_HEIGHT  = 1080

    img = gimp.image_list()[0]

    # assumes all layers are meant to be in same width/height as image size
    img_height = img.height
    img_width = img.width
    layers = img.layers
    layer_count = len(layers)

    # packs via best fit - tries to make a square
    if layer_count % 2 == 0:
        cols = layer_count / 2 
    else:
        cols = (layer_count - 1) / 2 

    final_height = cols * img_height
    final_width = cols * img_width

    # add new layer to draw on
    combined_layer = gimp.Layer(img,"Sprite Sheet",final_width,final_height,RGB_IMAGE,100,NORMAL_MODE)
    img.add_layer(combined_layer,0)

    col_count = 0
    combined_layer_offset_x = 0
    combined_layer_offset_y = 0
     
    # draw original pixel region in new layer
    for layer in layers:

        source_width = layer.width
        source_height = layer.height
        source_region = layer.get_pixel_rgn(0, 0, source_width, source_height, False, False)
        bytes_pp = len(source_region[0, 0])
        target_region = combined_layer.get_pixel_rgn(combined_layer_offset_x ,combined_layer_offset_y, source_width, source_height, True, True)

        source_pixels = array("B", source_region[0:source_width, 0:source_height])

        # draw pixel regions
        for x in range(0, source_width):
            for y in range(0, source_height):
                src_pos = (x + source_width * y) * bytes_pp
                dest_pos = (x + source_width * y) * bytes_pp
    
                
        target_region[0:source_width, 0:source_height] = source_pixels.tostring()
                

        # get offsets needed to fit in new layer
        if col_count == cols:
            col_count = 0
            combined_layer_offset_y += img_height
            combined_layer_offset_x = 0
        else:
            col_count += 1
            combined_layer_offset_x += img_width
		

    # display completed layer
    #pdb.gimp_display_new(img)
    combined_layer.flush()
    combined_layer.merge_shadow(True)
    combined_layer.update(0, 0, source_width, source_height)
    gimp.gimp_image_set_resolution(img, final_height, final_width)
    
    return

#Combine_Layers_To_Sheet()

gimpfu.register(
    "Combine To Sprite Sheet",
	"Combine all layers into a single sprite sheet - assumes all layers are the same size",
	"Combine all layers into a single sprite sheet - assumes all layers are the same size",
	"Brody Clark",
	"Brody Clark",
	"2022-2023",
	"<Image>/Tools",
	"RGB*, GRAY*",
	[],
	[],
	Combine_Layers_To_Sheet,
    menu = "<Image>/Tools"
    )


gimpfu.main()