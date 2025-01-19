"""
This script is a GIMP plugin that scales the current image using the xBRZ algorithm via a C++ .dll.
The xBRZ algorithm is a high-quality image scaling algorithm that is particularly
well-suited for pixel art. The plugin creates a new layer with the scaled image
and displays it in a new image window.
"""

import ctypes
import os
import sys
from gimpfu import *

# Load the shared library
if hasattr(sys, 'argv') and sys.argv[0]:
    script_path = os.path.abspath(sys.argv[0])
else:
    script_path = os.path.abspath('.')
dll_path = os.path.dirname(script_path)
xbrz_lib = ctypes.CDLL(dll_path + "\\xBRZ\\xBRZWrapper.dll")

# Define the xBRZ function prototype
xbrz_lib.Scale.argtypes = [
    ctypes.c_size_t,  # factor
    ctypes.POINTER(ctypes.c_uint32),  # src
    ctypes.POINTER(ctypes.c_uint32),  # trg
    ctypes.c_int,  # srcWidth
    ctypes.c_int,  # srcHeight
    ctypes.c_int,  # color format
    ctypes.c_int,  # yFirst
    ctypes.c_int   # yLast
]
xbrz_lib.Scale.restype = None

def scale_to_new_layer(image, drawable, scale_factor):
    pdb.gimp_image_undo_group_start(image)

    # Get the original dimensions
    width = int(image.width)
    height = int(image.height)

    # Get the pixel data from current visible layers
    region = drawable.get_pixel_rgn(0, 0, width, height, False, False)
    pixels = bytearray(region[0:width, 0:height])

    # Prepare the input and output arrays
    input_pixels = (ctypes.c_uint32 * (width * height)).from_buffer(pixels)

    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    output_pixels = (ctypes.c_uint32 * (new_width * new_height))()

    # Call the xBRZ function
    xbrz_lib.Scale(
        int(scale_factor),
        input_pixels,
        output_pixels,
        width,
        height,
        1,  # 1 corresponds to RGBA
        0,
        height
    )
    
    # Create a new image from the output pixels
    new_image = pdb.gimp_image_new(new_width, new_height, 0)
    new_layer = gimp.Layer(new_image, "Scaled Layer", new_width, new_height, RGBA_IMAGE, 100, NORMAL_MODE)
    new_image.add_layer(new_layer, 0)
    region_out = new_layer.get_pixel_rgn(0, 0, new_width, new_height, True, True)
    region_out[0:new_width, 0:new_height] = bytes(bytearray(output_pixels))
    
    # Make the new layer visible
    new_layer.flush()
    new_layer.merge_shadow(True)
    new_layer.update(0, 0, new_width, new_height)

    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_displays_flush()

    # Display the new image
    gimp.Display(new_image)
    
register(
    "xbrz_pixel_scaler",
    "Scale Images using xBRZ",
    "Creates a non-destructive xBRZ-scaled image of all visible layers.",
    "Brody Clark",
    "MIT License",
    "2025",
    "<Image>/Image/PixelToolkit/xBRZ Scale",
    "*",
    [
        (PF_SPINNER, "scale_factor", "Scale Factor", 2, (1, 6, 1))
    ],
    [],
    scale_to_new_layer)

main()
