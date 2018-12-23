import click

from file_formats.mtn import MountainToBitmap


@click.command()
@click.argument('f', type=click.Path(exists=True))
def main(f):
    MountainToBitmap.from_file(f).build()


if __name__ == '__main__':
    main()
