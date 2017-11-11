# https://media.readthedocs.org/pdf/pillow/stable/pillow.pdf
from PIL import ImageGrab

from flac.lib.color import ColorPrint

folderpath = '/Volumes/Media/tmp/folder.jpg'


def save_cb_image():
    img = ImageGrab.grabclipboard()
    if img:
        img.save(folderpath)
        ColorPrint.print_c('front saved!', ColorPrint.LIGHTCYAN)


def main():
    save_cb_image()


if __name__ == '__main__':
    main()
