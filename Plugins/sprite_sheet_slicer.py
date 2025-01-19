"""
A Gimp plugin that slices a tiled sprite-sheet into separate layers within a new image.
"""
import math
from gimpfu import *

def slice_sprite_sheet(image, drawable, width, height):
    if width < 4 or height < 4:
        gimp.message("The value you entered is too small.\
            \nPlease enter a value of at least 4 pixels")
        return
    
    original_width = drawable.width
    original_height = drawable.height
    if original_height < 4 or original_width < 4:
        gimp.message("The layer you chose is too small.\
            \nPlease select a layer of at least 8x8 pixels")
        return

    # Make sure ranges are valid
    width = clamp(4, original_width, width)
    height = clamp(4, original_height, height)
    if original_width % width != 0 or original_height % height != 0:
        gimp.message("The selected layer could not be completely sliced.\
            \n Make sure its width and height are divisble by the entered\
                width and height respectively")

    # Create new image
    new_img = pdb.gimp_image_new(width, height, 0)

    # Initialize variables for looping
    rows_count = int(math.floor(original_width / width))
    columns_clount = int(math.floor(original_height / height))
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
            pixel_region = get_pixel_region(drawable, combined_offset_x,
                                            combined_offset_x + width,
                                        combined_offset_y,
                                        combined_offset_y + height )
            draw_pixel_region(pixel_region, new_layer, 0, width, 0, height)
        
            # Make sure layer is a part of new image and draws correctly
            new_img.add_layer(new_layer,0)
            new_layer.merge_shadow(True)
            
            # Update values for next iteration
            combined_offset_y += height
            count += 1
        combined_offset_x += width
        combined_offset_y = 0

    # Show image
    gimp.Display(new_img)
    gimp.displays_flush()

def get_pixel_region(layer, x_begin, x_end, y_begin, y_end):
    region = layer.get_pixel_rgn(x_begin, y_begin, x_end, y_end, False, False)
    pixels = bytearray(region[:,:])
    return pixels

def clamp(mn, mx, num):
    if num < mn:
        num = mn
    elif num > mx:
        num = mx
    return num

def draw_pixel_region(pixels, layer, x_begin, x_end, y_begin, y_end):
    region_out = layer.get_pixel_rgn(x_begin, y_begin, x_end, y_end, True, True)
    height = y_end - y_begin
    width = x_end - x_begin
    region_out[0:width, 0:height] = bytes(pixels)
    
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
        (PF_INT, "width", "Tile Width", 0),
        (PF_INT, "height", "Tile Height", 0)
    ],
    [],
    slice_sprite_sheet)

main()