import io

from PIL import Image

from file_formats.structs.bitmap import bitmap_struct
from file_formats.structs.mtn import mtn_struct
from util import load_file_as_binary, unpad, mirror_array, rotate_matrix_90_degrees_left, \
    rotate_matrix_90_degrees_right, pad_matrix, path_to_filename


class BitmapToMountain:
    def __init__(self, bitmap_bytes, filename):
        self.filename = filename
        self.bitmap_bytes = bitmap_bytes
        self.bitmap_struct = bitmap_struct.parse(self.bitmap_bytes)

        self.sky_palette_value = self.bitmap_struct.pixels[-1][0]

    @classmethod
    def from_file(cls, path):
        return BitmapToMountain(
            load_file_as_binary(path),
            path_to_filename(path)
        )

    def bitmap_to_mtn_pixels(self):
        # 1. Rotate it to the left, because the pixels need to be structured as height slices
        # 2. Bitmaps are bottom to top, and mountains are top to bottom, so reverse/mirror the array
        # 3. Remove the sky pixels from the maxtrix rows.

        positioned_matrix = mirror_array(
            rotate_matrix_90_degrees_left(self.bitmap_struct.pixels)
        )

        return unpad(
            positioned_matrix, self.sky_palette_value
        )

    def build(self):
        pixels = self.bitmap_to_mtn_pixels()
        me_mtn_binary = mtn_struct.build(
            {
                'width': self.bitmap_struct.width,
                'minimum_bytes_per_row': min([len(subarray) for subarray in pixels]),
                'height': self.bitmap_struct.height,
                'sky_palette_index': self.sky_palette_value,
                'palette': self.bitmap_struct.palette,
                'pixels': pixels,
                'palette_and_image_size': 0
            }
        )
        with open(f'{self.filename.upper()}.MTN', 'wb') as file:
            file.write(me_mtn_binary)


class MountainToBitmap:
    def __init__(self, mountain_bytes, filename):
        self.mountain_bytes = mountain_bytes
        self.mountain_struct = mtn_struct.parse(mountain_bytes)

        self.filename = filename

    @classmethod
    def from_file(cls, path):
        return MountainToBitmap(
            load_file_as_binary(path),
            path_to_filename(path)
        )

    def padded_mirrored_rotated_pixels(self, pixels, height, pad_value):
        return rotate_matrix_90_degrees_right(
            mirror_array(
                pad_matrix(
                    pixels, height, pad_value
                )
            )
        )

    def build(self):
        padded_pixels = self.padded_mirrored_rotated_pixels(
            self.mountain_struct.pixels,
            self.mountain_struct.height,
            self.mountain_struct.sky_palette_index,
        )

        image = Image.open(
            io.BytesIO(
                bitmap_struct.build({
                    'width': self.mountain_struct.width,
                    'height': self.mountain_struct.height,
                    'palette': self.mountain_struct.palette,
                    'pixels': padded_pixels,
                    'bpp': 4,
                    'colors_used': 16,
                    'important_colors': 0,
                    'planes': 1
                })
            )
        )

        image.save(f'{self.filename}.bmp')
