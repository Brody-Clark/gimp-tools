
from gimpfu import *
import math

def Slice_Sprite_Sheet(layer, width, height):
   
    if width < 4 or height < 4:
        gimp.message("The value you entered is too small. Please enter a value of at least 4 pixels")
        return 
    
    original_width = layer.width
    original_height = layer.height

    if original_height < 4 or original_width < 4:
        gimp.message("The layer you chose is too small. Please select a layer of at least 8x8 pixels")
        return 

    # make sure ranges are valid
    width = Clamp(4,original_width, width)
    height = Clamp(4,original_height, height)

    if original_width % width != 0 or original_height % height != 0:
        gimp.message("The selected layer could not be completely sliced. Make sure its width and height are divisble by the entered width and height respectively")

    rows_count = int(math.floor(original_width / width))
    columns_clount = int(math.floor(original_height / height))
    
    # create new image
    new_img = pdb.gimp_image_new(width, height, 0)

    combined_offset_x = 0
    combined_offset_y = 0
    count = 0

    # draw new layers based on sections from original image
    for x in range(rows_count):
        for y in range(columns_clount):
             
             new_layer = gimp.Layer(new_img, "%s"%count, width, height, RGBA_IMAGE, 100, NORMAL_MODE)
             pixel_region = Get_Pixel_Region(layer, combined_offset_x, combined_offset_x + width, 
                                            combined_offset_y, combined_offset_y + height )
             Draw_Pixel_Region(pixel_region, new_layer, 0, width, 0, height)
            
             new_img.add_layer(new_layer,0)

             combined_offset_y += height
             count += 1

        combined_offset_x += width
        combined_offset_y = 0

    # show image
    gimp.Display(new_img)
    gimp.displays_flush()
    
    return
   
def Get_Pixel_Region(layer, x_begin, x_end, y_begin, y_end):
    pixel_region = []
    for x in range(x_begin,x_end):
            for y in range(y_begin,y_end):
                
                cur_pixel = pdb.gimp_drawable_get_pixel(layer,x,y)
                pixel_color = cur_pixel[1]
                pixel_size = cur_pixel[0]
                
                if pixel_size == 3:
                    pixel_size = 4
                    new_pixel_color =[pixel_color[0], pixel_color[1], pixel_color[2], 255]
                    pixel_color = new_pixel_color

                pixel_region.append([pixel_size, pixel_color])

    return pixel_region

def Clamp(min, max, num):

    if num < min:
        num = min
    elif num > max:
        num = max

    return num

def Draw_Pixel_Region(pixels, layer, x_begin, x_end, y_begin, y_end):
    index = 0
    for x in range(x_begin, x_end):
        for y in range(y_begin, y_end):

            pdb.gimp_drawable_set_pixel(layer, x, y, pixels[index][0], pixels[index][1])
            index += 1
    return


register(
    "export-as-sprite-sheet",
    "Slice sprite sheet into new image",
    "Slice sprite sheet into new image - Assumes all tiles will be the same size. Minimum size is 4x4",
    "Brody Clark",
    "Brody Clark",
    "2024",
    "Slice Sprite Sheet...",
    "*",
    [
        (PF_LAYER, "layer", "Layer to Slice", None),
        (PF_INT, "width", "Tile Width", 0),
        (PF_INT, "height", "Tile Height", 0)
    ],
    [],
    Slice_Sprite_Sheet,
    menu="<Image>/Image/Sprite Sheet Slicer"
    )

main()