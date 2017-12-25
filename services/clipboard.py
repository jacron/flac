from flac.lib.color import ColorPrint
from PIL import ImageGrab

from flac.services import openpath
from flac.settings import COVER_PATH, TMP_PATH, SCORE_FRAGMENT_PATH

rug = 0


def save_score_fragment(code):
    img = ImageGrab.grabclipboard()
    if img:
        img.save(SCORE_FRAGMENT_PATH.format(code))


def crop_front(img):
    width = img.size[0]
    height = img.size[1]
    fbox = (width / 2 + rug, 0, width, height)
    return img.crop(fbox)


def crop_back(img):
    width = img.size[0]
    height = img.size[1]
    bbox = (0, 0, width / 2 - rug, height)
    return img.crop(bbox)


def save_cb_images(cover, nback):
    img = ImageGrab.grabclipboard()
    if img:
        front = crop_front(img)
        back = crop_back(img)
        front.save(COVER_PATH.format(cover))
        back.save(COVER_PATH.format(nback))
        openpath(TMP_PATH)
    else:
        ColorPrint.print_c('no valid image on clipboard', ColorPrint.RED)


def save_cb_image(cover):
    img = ImageGrab.grabclipboard()
    if img:
        img.save(COVER_PATH.format(cover))
        openpath(TMP_PATH)


