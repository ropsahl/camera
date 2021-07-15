import glob
import os

import numpy as np
import requests
import time
from PIL import Image

baseHeight = 80
window_size = 12
windowSumLimit = window_size * 30
windowDiffLimit = 500
filename_utsikt = "./public/utsikt.jpg"


def crop(filename):
    if filename:
        print("Cropping0:" + str(filename))

        img = Image.open(filename)
        print("Cropping1:" + str(filename))
        w, h = img.size
        print("Cropping2:" + str(filename))
        left = w / 6
        print("Cropping3:" + str(filename))
        top = 2 * h / 6
        print("Cropping4:" + str(filename))
        right = 4 * w / 6
        bottom = 3.8 * h / 6
        print("Cropping5:" + str(filename))
        cropped = img.crop((left, top, right, bottom))
        print("Cropped6:" + str(filename))
        img.close()
        print("closed:" + str(filename))
        cropped.save(filename)
        print("saved cropped:" + str(filename))


def take_snap():
    print("snap")
    config = {
        "config": {
            "meter": "average"
        },
        "image": {
            "height": 2464,
            "width": 3280,
            "rotation": 270
        }
    }
    res = requests.post("http://localhost:8100/camera_config/camera", json=config)
    if res.ok:
        filename = './public/' + res.json()['image']['fileName']
        crop(filename)
        return filename


def resampled_array(filename):
    if filename:
        img = Image.open(filename)
        hpercent = (baseHeight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseHeight), Image.ANTIALIAS)
        return np.array([x for sets in list(img.getdata())
                         for x in sets])


def delete_if_no_change(prev_all_pix, filename):
    if filename:
        new_pix_arr = resampled_array(filename)
        pix_diff = 0
        for i in range(window_size, len(new_pix_arr)):
            if abs(np.sum(new_pix_arr[i - window_size:i]) - np.sum(prev_all_pix[i - window_size:i])) > windowSumLimit:
                pix_diff += 1
        if pix_diff > windowDiffLimit:
            print("delete_if_no_change, pix_diff: " + str(pix_diff) + ", keeping: " + str(filename))
            os.remove(filename_utsikt)
            os.symlink(filename, filename_utsikt)
            return new_pix_arr
        if os.path.exists(filename):
            print("delete_if_no_change, pix_diff: " + str(pix_diff) + ", removing: " + str(filename))
            os.remove(filename)
        print("Keeping: " + str(filename))
        return prev_all_pix


def initialize():
    all_files = sorted(glob.glob("./public/*.jpg"))
    return resampled_array(all_files[len(all_files) - 1])


def periodic():
    prev_arr = initialize()
    while True:
        prev_arr = delete_if_no_change(prev_arr, take_snap())
        time.sleep(60)


periodic()
