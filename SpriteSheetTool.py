#!/usr/bin/python3

from gimpfu import *
import math
import numpy as np
from collections import namedtuple 

def Channel_Data(layer):
    w,h=layer.width,layer.height
    region=layer.get_pixel_rgn(0, 0, w,h)
    pixChars=region[:,:]
    bpp=region.bpp
    return np.frombuffer(pixChars,dtype=np.uint8).reshape(w,h,bpp)

def Draw_Result_Layer(image,result_layer,result, region_start_x, region_start_y):
    rlBytes=np.uint8(result).tobytes()
    region=result_layer.get_pixel_rgn(region_start_x, region_start_x, (region_start_x + result_layer.width), (region_start_y + result_layer.height),True)
    region[:,:]=rlBytes

def Combine_Layers_To_Sheet():

    MAX_WIDTH   = 1920
    MAX_HEIGHT  = 1080

    # just packs via best fit - tries to make a square
    img = gimp.image_list()[0]

    # assumes all layers are meant to be in same width/height as image size
    img_height = img.height
    img_width = img.width

    layers = img.layers
   
    layer_count = len(layers)

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

    
     
    # draw each original pixel in new layer
    for layer in layers:
        Draw_Result_Layer(img,combined_layer,Channel_Data(layer),combined_layer_offset_x, combined_layer_offset_y)
       
        if col_count == cols:
            col_count = 0
            combined_layer_offset_y += img_height
            combined_layer_offset_x = 0
        else:
            col_count += 1
            combined_layer_offset_x += img_width
		

    # display completed layer
    display = pdb.gimp_display_new(img)
    #gimp.displays_flush()
    gimp.gimp_image_set_resolution(img, final_height, final_width)
    
    return

Combine_Layers_To_Sheet()

register(
	"Sprite Sheet",
	"Combine all layers into sprite sheet - assumes all layers are the same size",
	"Combine all layers into sprite sheet - assumes all layers are the same size",
	"Brody Clark",
	"Brody Clark",
	"2022-2023",
	"<Image>/Combine To Sprite Sheet",
	"RGB*, GRAY*",
	[],
	[],

	Combine_Layer_To_Sheet, menu = "<Image>, Combine To Sprite Sheet"
    )

main()