from flac.lib.color import ColorPrint
from PIL import ImageGrab

from flac.services import openpath
from flac.services.path import create_componist_path, create_performer_path
from flac.settings import COVER_PATH, TMP_PATH, SCORE_FRAGMENT_PATH, PERSON_FILE
from ..db import get_componist_path, get_performer_path
import os

rug = 0


def save_score_fragment(code):
    img = ImageGrab.grabclipboard()
    if img:
        img.save(SCORE_FRAGMENT_PATH.format(code))


def delete_score_fragment(code):
    img_path = SCORE_FRAGMENT_PATH.format(code)
    os.remove(img_path)


def get_person_image_path(id, type):
    image_path = None
    if type == 'componist':
        image_path = create_componist_path(id)
    if type == 'performer':
        image_path = create_performer_path(id)
    return image_path


def save_person(id, type):
    img = ImageGrab.grabclipboard()
    if img:
        image_path = get_person_image_path(id, type)
        if image_path:
            img.save(image_path + PERSON_FILE)
            return True
        else:
            ColorPrint.print_c('no valid path for this person', ColorPrint.RED)
    else:
        ColorPrint.print_c('no valid image on clipboard', ColorPrint.RED)
    return False


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


