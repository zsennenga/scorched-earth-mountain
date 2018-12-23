import math

from construct import *

# "Why not use PIL" - PIL can read, but, as far as I could tell, won't natively create
# real, true, 16 color bmp. You can make a 16 color image just fine, but when you save it,
# it'll be formatted as a 256 color image. Maybe I'm wrong!
bitmap_struct = Struct(

    "signature" / Const(b"BM"),
    "file_size" / Rebuild(Int32ul, lambda ctx: 14 + 40 + int((ctx.height * ctx.width * ctx.bpp) / 8)),
    Padding(4),
    "data_offset" / Rebuild(Int32ul, 14 + 40 + ((2 ** this.bpp if this.bpp <= 8 else 0) * 4)),
    "header_size" / Const(40, Int32ul),
    "width" / Int32sl,
    "height" / Int32sl,
    "planes" / Int16ul,
    "bpp" / Const(4, Int16ul),  # bits per pixel
    "compression" / Const(0, Int32ul),
    "image_data_size" / Rebuild(Int32ul, lambda ctx: int((ctx.height * ctx.width * ctx.bpp) / 8)),
    "horizontal_dpi" / Rebuild(Int32ul, lambda ctx: int(math.ceil(39.3701 * 72 * ctx.width))),
    "vertical_dpi" / Rebuild(Int32ul, lambda ctx: int(math.ceil(39.3701 * 72 * ctx.height))),
    "colors_used" / Int32ul,
    "important_colors" / Int32ul,
    "palette" / Array(
        lambda ctx: 2 ** ctx.bpp if ctx.bpp <= 8 else 0,
        Struct(
            "B" / Int8ul,
            "G" / Int8ul,
            "R" / Int8ul,
            Padding(1)
        )
    ),
    "pixels" / Array(this.height, Aligned(4, Bitwise(Aligned(8, Array(this.width, Nibble))))),
)