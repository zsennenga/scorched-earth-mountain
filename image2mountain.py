import click

from file_formats.bmp import ImageTo4BitBitmap
from file_formats.mtn import BitmapToMountain
from util import path_to_filename


@click.command()
@click.argument('f', type=click.Path(exists=True))
def main(f):
    bitmap_bytes = ImageTo4BitBitmap(f).to_bytes()

    BitmapToMountain(
        bitmap_bytes,
        path_to_filename(f)
    ).build()


if __name__ == '__main__':
    main()
