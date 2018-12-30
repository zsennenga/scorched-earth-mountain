# Scorched Earth Mountain Creator
Utilities to create and manipulate mountains from the program "Scorched Earth"

image2mountain.py will take any image format Pillow can support (effectively, anything).

mountain2image.py will output a 16 color bitmap.

## Image Preparation and Limitations

The only transformation that needs to be done is to remove the background from your image so Scorched Earth can fill it with sky.

Any tool can be used to do this, but there are some limitations to be aware of.

Scorched earth can only handle sky if there's an uninterrupted line between the top of the image and the "subject" of the image.
This means it can't handle concave shapes - think of objects shaped like a C. The impact of this will be concave shapes will be still contain whatever color the sky is.

Sky is detected via the top left pixel color, so make sure the very top left pixel of your image is the color of sky.