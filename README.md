# GIMP PixelToolkit

Collection of pixel art-focused plugins for GIMP Image Editing Software.

## Adding Plugins to GIMP

1. Locate your GIMP plug-in directory, this can be found within GIMP under `Edit > Preferences > Folders > Plug-ins`
2. Copy all files and folders from this project's `Plugins` directory to the GIMP `plug-ins` directory.
3. Restart GIMP.

## Included Plugins

### Sprite Sheet Exporter

- Allows you to combine all working layers of an image into a packed sprite sheet and export it to a chosen folder. Original image and layers remain unchanged.
- Located under `Image > PixelToolkit > Export As Sprite Sheet`

<img src="resources/Export_Before.png" alt="Export Demo" width="45%">

### Sprite Sheet Slicer

- Simple sprite sheet utility designed to divide a packed tile sheet into individual layers.
- Located under `Image > PixelToolkit > Slice Sprite Sheet`

<img src="resources/Slice_Sprite_Sheet_UI.png" alt="Slicer UI" width="35%">

<img src="resources/Slice_Sprite_Sheet_After.png" alt="Slicer Before" width="35%">

### xBRZ Scaler

- Creates a non-destructive xBRZ-scaled image of active layer
- Located under `Image > PixelToolkit > xBRZ Scale`

<img src="resources/xBRZ_Scaler_Before.png" alt="xBRZ Before" width="25%">32x32
  
<img src="resources/xBRZ_Scaler_After.png" alt="xBRZ After" width="35%">128x128
