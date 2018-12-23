from PIL import Image

from file_formats.structs.bitmap import bitmap_struct


class ImageTo4BitBitmap:
    def __init__(self, path):
        self.base_image = Image.open(path)

    def to_bytes(self):
        palette_image = self.base_image.convert('P', palette=Image.ADAPTIVE, colors=16)

        pixel_data = palette_image.load()

        width = palette_image.size[0]
        height = palette_image.size[1]

        pixels = []

        for y in range(height):
            subarray = []
            for x in range(width):
                subarray.append(pixel_data[x, y])

            pixels.append(subarray)

        palette = []
        raw_palette = palette_image.getpalette()

        for i in range(16):
            offset = i * 3
            color = {
                'R': raw_palette[offset],
                'G': raw_palette[offset + 1],
                'B': raw_palette[offset + 2]
            }
            palette.append(color)

        return bitmap_struct.build({
            'width': width,
            'height': height,
            'bpp': 4,
            'colors_used': 16,
            'palette': palette,
            'pixels': list(reversed(pixels)),
            'important_colors': 0,
            'planes': 1
        })
