# https://media.readthedocs.org/pdf/pillow/stable/pillow.pdf
from PIL import ImageGrab

from flac.lib.color import ColorPrint

"""
copy pdf to clipboard
save left side to back.jpg
save right side to folder.jpg
"""
backpath = '/Volumes/Media/tmpscan/back.jpg'
folderpath = '/Volumes/Media/tmpscan/folder.jpg'


def save_cb_image():
    img = ImageGrab.grabclipboard()
    rug = 170
    if img:
        print(img.size)
        width = img.size[0]
        height = img.size[1]

        bbox = (0, 0, width / 2 - rug, height)
        back = img.crop(bbox)
        back.save(backpath)
        ColorPrint.print_c('back saved!', ColorPrint.BROWN)

        fbox = (width / 2 + rug, 0, width, height)
        front = img.crop(fbox)
        front.save(folderpath)
        ColorPrint.print_c('folder saved!', ColorPrint.BLUE)
    else:
        ColorPrint.print_c('No image on clipboard!', ColorPrint.RED)



def main():
    save_cb_image()


if __name__ == '__main__':
    main()
