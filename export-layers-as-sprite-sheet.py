
from gimpfu import *
import math
import os

FILE_TYPES = ["png", "jpeg"]
PACK_TYPES = ["By Row", "By Columns", "Best Fit"]

def Export_Layers_As_Sheet(image, dir, file_name, file_type):
  
    # check file path is valid
    if not os.path.isdir(dir):
            os.makedirs(dir)

    # check image is valid
    if image == None:
        img = gimp.image_list()[0]
    else:
        img = image

    # check user-given file name
    if file_name == "":
        file_name = image.name 

    # assumes all layers are meant to be in same width/height as their image size
    img_height = img.height
    img_width = img.width
    layers = img.layers
    layer_count = len(layers)

    # packs via best fit - tries to make a square
    # TODO: let user select By Rows or By Columns with number input, or Best fit
    cols = math.ceil(math.sqrt(layer_count))
    cols = int(cols)

    final_height = cols * img_height
    final_width = cols * img_width

    # add new image and layer to draw on
    new_img = pdb.gimp_image_new(final_width, final_height, 0)
    combined_layer = gimp.Layer(new_img,"Sprite Sheet",final_width,final_height,RGBA_IMAGE,100,NORMAL_MODE)
    new_img.add_layer(combined_layer,0)

    col_count = 1
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
            col_count = 1
            combined_layer_offset_y += img_height
            combined_layer_offset_x = 0
        else:
            col_count += 1
            combined_layer_offset_x += img_width
		

    # export and cleanup
    combined_layer = pdb.gimp_image_merge_visible_layers(new_img, CLIP_TO_IMAGE)
    file_name = '%s.%s'%(file_name,FILE_TYPES[file_type])
    pdb.gimp_file_save(new_img, combined_layer, os.path.join(dir, file_name), file_name)
    pdb.gimp_image_delete(new_img)


register(
    "export-as-sprite-sheet",
    "Combine layers into sprite sheet and export",
    "Combine layers into sprite sheet and export - combines layers into a square best-fit sheet. Assumes all layers are same size",
    "Brody Clark",
    "Brody Clark",
    "2024",
    "Export As Sprite Sheet...",
    "*",
    [
        (PF_IMAGE, "image", "Input Image", None),
        (PF_DIRNAME, "dir", "Export Location", ""),
        (PF_STRING, "file_name", "Exported File Name", ""),
        (PF_OPTION, "file_type", "Exported File Type", 0, FILE_TYPES),
    ],
    [],
    Export_Layers_As_Sheet,
    menu="<Image>/Image/Export As Sprite Sheet"
    )

main()