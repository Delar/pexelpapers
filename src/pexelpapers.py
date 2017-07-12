# Entry point
import imghdr
import os
import platform
import random
import re
import struct

import scraping
import os_specific

IMAGES_PATH = os.getcwd()

def main():
    image_urls = scraping.get_image_urls()
    screen_size = get_screen_size()
    while True:
        random_image_url = random.choice(image_urls)
        random_image = download_images(IMAGES_PATH, [random_image_url])[0]
        screen_size = get_screen_size()
        image_size = get_image_size(random_image)
        if image_size[0] >= screen_size[0] and image_size[1] >= screen_size[1]:
            set_wallpaper(random_image)
            os.remove(random_image)
            break


def set_wallpaper(image_path):
    if platform.system() == 'Windows' and platform.release() == '10':
        os_specific.set_wallpaper_windows(image_path)
    else:
        raise NotImplementedError


def download_images(path, urls):
    """ Will not download if already exists in path.

    :param path: path to download to
    :param urls: images urls
    :return: list of full names of downloaded files
    """
    downloaded = []
    if not os.path.isdir(path):
        os.mkdir(path)
    for url in urls:
        file_name = re.split('/', url)[-1]
        full_path = path + file_name
        scraping.send_get_request(url, full_path)
        downloaded.append(full_path)
    return downloaded


def get_screen_size():
    if platform.system() == 'Windows' and platform.release() == '10':
        return os_specific.detect_resolution_windows()
    else:
        raise NotImplementedError


# Shamelessly ripped off StackOverflow
def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height


if __name__ == '__main__':
    main()