import glob
import os

import numpy as np
from PIL import Image

baseHeight = 80
windowSize = 12
windowSumLimit = windowSize * 30
windowDiffLimit = 2000

prev_all_pix = []
for file in glob.glob("./importedPictures/*.jpg"):
    img = Image.open(file)
    hpercent = (baseHeight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseHeight), Image.ANTIALIAS)
    allPix = [x for sets in list(img.getdata())
              for x in sets]
    npa = np.array(allPix)
    pixDiff = 0
    if len(prev_all_pix) > 0:
        for i in range(windowSize, len(allPix)):
            if abs(np.sum(npa[i - windowSize:i]) - np.sum(prev_all_pix[i - windowSize:i])) > windowSumLimit:
                pixDiff += 1
    if pixDiff > windowDiffLimit:
        img.save(
            os.path.join(os.path.dirname(file), "resampled",
                         os.path.splitext(os.path.basename(file))[0] + "_" + str(pixDiff) + ".jpg"))
    prev_all_pix = npa


def manipuler():
    # split the image into individual bands
    source = img.split()

    R, G, B = 0, 1, 2

    # select regions where red is less than 100
    mask = source[R].point(lambda i: i < 100 and 255)

    # process the green band
    out = source[G].point(lambda i: i * 0.8)

    # paste the processed band back, but only where red was < 100
    source[G].paste(out, None, mask)

    # build a new multiband image
    im = Image.merge(img.mode, source)

    img.save('resized_image.jpg')
