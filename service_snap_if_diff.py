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


def take_snap():
    print("snap")
    config = {
        "config": {
            "meter": "average"
        },
        "image": {
            "height": 768,
            "width": 1024,
            "rotation": 270
        }
    }
    res = requests.post("http://localhost:8100/camera_config/camera", json=config)
    if res.ok:
        return res.json()['image']['fileName']


def resampled_array(filename):
    print("resampled_array: " + str(filename))
    if filename:
        img = Image.open(filename)
        hpercent = (baseHeight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseHeight), Image.ANTIALIAS)
        return np.array([x for sets in list(img.getdata())
                         for x in sets])


def delete_if_no_change(prev_all_pix, filename):
    print("delete_if_no_change: " + str(filename))
    if filename:
        new_pix_arr = resampled_array(filename)
        pix_diff = 0
        for i in range(window_size, len(new_pix_arr)):
            if abs(np.sum(new_pix_arr[i - window_size:i]) - np.sum(prev_all_pix[i - window_size:i])) > windowSumLimit:
                pix_diff += 1
        print("delete_if_no_change, pix_diff: " + str(pix_diff))
        if pix_diff > windowDiffLimit:
            os.remove(filename_utsikt)
            os.symlink(filename, filename_utsikt)
            return new_pix_arr
        if os.path.exists(filename):
            os.remove(filename)
        return prev_all_pix


def initialize():
    all_files = sorted(glob.glob("./public/*.jpg"))
    return resampled_array(all_files[len(all_files) - 1])


def periodic():
    prev_arr = initialize()
    while True:
        prev_arr = delete_if_no_change(prev_arr, './public/' + take_snap())
        time.sleep(60)


periodic()
