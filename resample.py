from PIL import Image

baseHeight = 80
windowSize = 12
windowSumLimit = windowSize * 30
windowDiffLimit = 2000
'./importedPictures\\utsikt_2021-02-07_135452.jpg'
prev_all_pix = []
img = Image.open(".\\importedPictures\\utsikt_2021-07-15_153906.jpg")
w, h = img.size
left = w / 6
top = 2*h / 6
right = 4 * w / 6
bottom = 3.8 * h / 6
cropped = img.crop((left, top, right, bottom))
img.close()
cropped.save(".\\importedPictures\\cropped.jpg")


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
