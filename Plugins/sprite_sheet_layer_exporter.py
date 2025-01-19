import math
import os
from gimpfu import *

FILE_TYPES = ["png", "jpeg"]
RGB = 3
RGBA = 4
OPAQUE_ALPHA = 255

def export_layers_as_spritesheet(image, drawable, export_dir, file_name, file_type):

    # Check file path is valid
    if not os.path.isdir(export_dir):
        os.makedirs(export_dir)

    # Check user-given file name
    if file_name == "":
        file_name = image.name
    else:
        file_name = file_name.strip()
 
    # Packs via best fit - tries to make a square
    layers = image.layers
    layer_count = len(layers)

    img_height = image.height
    img_width = image.width

    cols = math.ceil(math.sqrt(layer_count))
    cols = int(cols)

    final_height = cols * img_height
    final_width = cols * img_width

    # Add new image and layer to draw on
    new_img = pdb.gimp_image_new(final_width, final_height, 0)
    combined_layer = gimp.Layer(new_img,
                                "Sprite Sheet",
                                final_width,
                                final_height,
                                RGBA_IMAGE,
                                100,
                                NORMAL_MODE)
    new_img.add_layer(combined_layer,0)

    col_count = 1
    combined_layer_offset_x = 0
    combined_layer_offset_y = 0

    # Draw original pixels in new layer
    for layer in layers:
        source_width = layer.width
        source_height = layer.height
        for x in range(0, source_width):
            for y in range(0, source_height):
                cur_pixel = pdb.gimp_drawable_get_pixel(layer,x,y)
                pixel_color = cur_pixel[1]
                pixel_size = cur_pixel[0]
                
                # Force RGB pixles to be RGBA
                if pixel_size == RGB:
                    pixel_size = RGBA
                    new_pixel_color =[pixel_color[0],
                                      pixel_color[1],
                                      pixel_color[2],
                                      OPAQUE_ALPHA]
                    pixel_color = new_pixel_color

                pdb.gimp_drawable_set_pixel(combined_layer,
                                            combined_layer_offset_x + x,
                                            combined_layer_offset_y + y,
                                            pixel_size,
                                            pixel_color)

        # Get offsets needed to fit in new layer
        if col_count == cols:
            col_count = 1
            combined_layer_offset_y += img_height
            combined_layer_offset_x = 0
        else:
            col_count += 1
            combined_layer_offset_x += img_width
		
    # Export and cleanup
    combined_layer = pdb.gimp_image_merge_visible_layers(new_img, CLIP_TO_IMAGE)
    file_name = "{}.{}".format(file_name, FILE_TYPES[file_type])
    export_path = os.path.join(export_dir, file_name)
    pdb.gimp_file_save(new_img, combined_layer, export_path, file_name)
    pdb.gimp_image_delete(new_img)

register(
    "export-as-sprite-sheet",
    "Combine layers into sprite sheet and export",
    "Combine layers into sprite sheet and export - combines layers into a square best-fit sheet.\
        Assumes all layers are same size and image is RGBA",
    "Brody Clark",
    "MIT License",
    "2025",
    "<Image>/Image/PixelToolkit/Export As Sprite Sheet",
    "*",
    [
        # (PF_IMAGE, "image", "Input Image", None),
        (PF_DIRNAME, "export_dir", "Export Location", ""),
        (PF_STRING, "file_name", "Exported File Name", ""),
        (PF_OPTION, "file_type", "Exported File Type", 0, FILE_TYPES),
    ],
    [],
    export_layers_as_spritesheet)

main()