"""
A Gimp plugin that slices a tiled sprite-sheet into separate layers within a new image.
"""
import math
from gimpfu import *

RGB = 3
RGBA = 4
OPAQUE_ALPHA = 255

def slice_sprite_sheet(layer, width, height):
    if width < 4 or height < 4:
        gimp.message("The value you entered is too small.\
            \nPlease enter a value of at least 4 pixels")
        return
    
    original_width = layer.width
    original_height = layer.height

    if original_height < 4 or original_width < 4:
        gimp.message("The layer you chose is too small.\
            \nPlease select a layer of at least 8x8 pixels")
        return

    # Make sure ranges are valid
    width = clamp(4,original_width, width)
    height = clamp(4,original_height, height)

    if original_width % width != 0 or original_height % height != 0:
        gimp.message("The selected layer could not be completely sliced.\
            \n Make sure its width and height are divisble by the entered\
                width and height respectively")

    rows_count = int(math.floor(original_width / width))
    columns_clount = int(math.floor(original_height / height))
    
    # create new image
    new_img = pdb.gimp_image_new(width, height, 0)

    combined_offset_x = 0
    combined_offset_y = 0
    count = 0

    # Draw new layers based on sections from original image
    for x in range(rows_count):
        for y in range(columns_clount):
             new_layer = gimp.Layer(new_img,
                                    "%s"%count,
                                    width,
                                    height,
                                    RGBA_IMAGE,
                                    100,
                                    NORMAL_MODE)
             pixel_region = get_pixel_region(layer, combined_offset_x,
                                             combined_offset_x + width,
                                            combined_offset_y,
                                            combined_offset_y + height )
             draw_pixel_region(pixel_region, new_layer, 0, width, 0, height)
            
             new_img.add_layer(new_layer,0)

             combined_offset_y += height
             count += 1

        combined_offset_x += width
        combined_offset_y = 0

    # Show image
    gimp.Display(new_img)
    gimp.displays_flush()
    
    return
   
def get_pixel_region(layer, x_begin, x_end, y_begin, y_end):
    pixel_region = []
    for x in range(x_begin,x_end):
            for y in range(y_begin,y_end):
                cur_pixel = pdb.gimp_drawable_get_pixel(layer,x,y)
                pixel_color = cur_pixel[1]
                pixel_size = cur_pixel[0]
                
                if pixel_size == RGB:
                    pixel_size = RGBA
                    new_pixel_color =[pixel_color[0],
                                      pixel_color[1],
                                      pixel_color[2],
                                      OPAQUE_ALPHA]
                    pixel_color = new_pixel_color

                pixel_region.append([pixel_size, pixel_color])

    return pixel_region

def clamp(mn, mx, num):
    if num < mn:
        num = mn
    elif num > mx:
        num = mx

    return num

def draw_pixel_region(pixels, layer, x_begin, x_end, y_begin, y_end):
    index = 0
    for x in range(x_begin, x_end):
        for y in range(y_begin, y_end):

            pdb.gimp_drawable_set_pixel(layer, x, y, pixels[index][0], pixels[index][1])
            index += 1
    return


register(
    "slice-sprite-sheet",
    "Slice sprite sheet into new image",
    "Slice sprite sheet into new image - Assumes all tiles will be the same size.\
        Minimum size is 4x4",
    "Brody Clark",
    "MIT License",
    "2025",
    "<Image>/Image/PixelToolkit/Slice Sprite Sheet",
    "*",
    [
        (PF_LAYER, "layer", "Layer to Slice", None),
        (PF_INT, "width", "Tile Width", 0),
        (PF_INT, "height", "Tile Height", 0)
    ],
    [],
    slice_sprite_sheet)

main()