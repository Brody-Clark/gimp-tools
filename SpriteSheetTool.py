#!/usr/bin/env python

from gimpfu import *
import math
from ast import literal_eval
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
        cols = (layer_count + 1) / 2 
    cols -= 1

    final_height = cols * img_height
    final_width = cols * img_width

    # add new layer to draw on
    combined_layer = gimp.Layer(img,"Sprite Sheet",final_width,final_height,RGBA_IMAGE,100,NORMAL_MODE)
    img.add_layer(combined_layer,0)

    col_count = 0
    combined_layer_offset_x = 0
    combined_layer_offset_y = 0

    # draw original pixel region in new layer
    for layer in layers:
        combined_layer.update(0, 0, final_width, final_height)
    
        source_width = layer.width
        source_height = layer.height
       
        for x in range(0,source_width):
            for y in range(0,source_height):
                cur_pixel = pdb.gimp_drawable_get_pixel(layer,x,y)
                pixel_color = cur_pixel[1]
                pixel_size = cur_pixel[0]
                
                if pixel_size == 3:
                    pixel_size = 4
                    new_pixel_color =[pixel_color[0], pixel_color[1], pixel_color[2], 255]
                    pixel_color = new_pixel_color

                pdb.gimp_drawable_set_pixel(combined_layer,combined_layer_offset_x + x, combined_layer_offset_y + y, pixel_size, pixel_color)

        # get offsets needed to fit in new layer
        if col_count == cols:
            col_count = 0
            combined_layer_offset_y += img_height
            combined_layer_offset_x = 0
        else:
            col_count += 1
            combined_layer_offset_x += img_width
		

    # display completed layer
    combined_layer.flush()
    combined_layer.update(0, 0, final_width, final_height)
    img.resize(final_width, final_height, 0,0)
    new_image = pdb.gimp_image_duplicate(img)   
    combined_layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
    pdb.gimp_file_save(new_image, combined_layer, 'F:/Development/Gimp/temp/test.png', '?')
    pdb.gimp_image_delete(new_image)

Combine_Layers_To_Sheet()


# gimpfu.register(
#     "Combine To Sprite Sheet",
# 	"Combine all layers into a single sprite sheet - assumes all layers are the same size",
# 	"Combine all layers into a single sprite sheet - assumes all layers are the same size",
# 	"Brody Clark",
# 	"Brody Clark",
# 	"2022-2023",
# 	"<Image>/Tools",
# 	"RGB*, GRAY*",
# 	[],
# 	[],
# 	Combine_Layers_To_Sheet,
#     menu = "<Image>/Tools"
#     )


# gimpfu.main()