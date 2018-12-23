from construct import *

mtn_struct = Struct(
    "signature" / Const(b"MT\xbe\xef"),
    "unknown_const_256" / Const(256, Int16ul) * "Probably part of the signature",
    "width" / Int16ul,
    "minimum_bytes_per_row" / Int16ul * "Likely used to aid resizing",
    "height" / Int16ul * "Seems to be decreased by 1 when using the standard builder. Bug?",
    "color_count" / Const(16, Int16ul),
    "palette_and_image_size" / Int16ul * "This seems to be unused - and it bugs out with larger images. You can easily exceed a short, even with the default generator",
    "sky_palette_index" / Int16ul * "This is the palette index referring to what the sky was",
    "unknowns_16" / Struct(
        "unknown_3" / Int16ul * "This doesn't seem to be used, and doesn't always vary between mtns",
        "unknown_4" / Int16ul * "This doesn't seem to be used, and doesn't always vary between mtns",
        "unknown_5" / Int16ul * "This doesn't seem to be used, and doesn't always vary between mtns",
    ),
    "palette" / Array(
        16,
        Struct(
            "R" / Int8ul,
            "G" / Int8ul,
            "B" / Int8ul,
        )
    ) * "Identical to a standard bitmap palette, except for the order of the pixels",
    "pixels" / Array(
        this.width,
        FocusedSeq(
            "items",
            "count" / Rebuild(Int16ul, len_(this.items)),
            "items" / Bitwise(
                Aligned(
                    8,
                    Array(
                        this .count,
                        Nibble
                    )
                )
            ),
        )
    ) * """
    There's a lot going on here.
    
    Conceptually, it's very similar to a standard bitmap 16 color image.
    
    However, in terms of storage it's quite different.
    
    Pixels are stored as vertical slices rather than horizontal slices, with the first value representing the bottommost pixel.
    
    In addition, they're stored leftmost to rightmost. 
    This is logical, but is a break from bitmaps, insomuch that bitmaps are stored logically reversed, as bottom-to-top.
    
    Thus, the pixel at 0,0 is equivalent to 0, 0 in the resulting image, identical to bitmap.
    
    Other than the pixel ordering, there's one more interesting bit, and it's the stripping of sky pixels from the pixel data.
    
    Each vertical slice is stored as a short representing how many nibbles make up this vertical slice. 
    The maximum value is equal to the height of the image.
    
    Each nibble is an index into the palette that represents the color of the pixel in question.
    
    You might notice this implies that a vertical slice can contain fewer pixels than the height.
    
    This is to accommodate sky. In the game, sky is the negative space in the image, the background.
    
    Recall vertical slices are stored top to bottom, thus, if you only have 50 pixels in a slice, 
    that means the remaining 50 are sky.
    
    Sky is determined by sampling the upper left pixel in the original image to capture the palette index.
    This is stored in sky_palette_index value in the structure.
    
    For each vertical slice, starting the from the right side, pixel values are removed until a non-sky palette value is found.
    
    Thus, if 0 is the sky palette value, and the following is a raw vertical slice:
    
    [0, 1, 0, 0, 0]
    
    would be stored as:
    
    [0, 1]    
    """
)
