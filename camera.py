# https://picamera.readthedocs.io/en/release-1.13/_modules/picamera/camera.html

import datetime

from picamera import PiCamera, Color
from time import sleep


def brightness(camera):
    for i in range(100):
        camera.annotate_text = "Brightness: %s" % i
        camera.brightness = i
        sleep(0.1)


def contrast(camera):
    for i in range(100):
        camera.annotate_text = "Contrast: %s" % i
        camera.contrast = i
        sleep(0.1)


def effects(camera):
    for effect in camera.IMAGE_EFFECTS:
        camera.image_effect = effect
        camera.annotate_text = "Effect: %s" % effect
        sleep(5)


def exposuremode(camera):
    for m in camera.EXPOSURE_MODES:
        camera.exposure_mode = m
        sleep(2)


def capture(camera):
    dateNow = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    sleep(2)
    camera.capture('/home/pi/utsikt/' + dateNow + '.jpg')


def snap(config):
    print(config)
    with PiCamera() as camera:
        camera.rotation = config['image']['rotation']
        camera.resolution = (config['image']['width'], config['image']['height'])
        camera.image_effect = config['config']['imageEffects']
        camera.contrast = config['config']['contrast']
        camera.brightness = config['config']['brightness']
        camera.exposure_mode = config['config']['exposure']
        camera.annotate_text_size = 50
        camera.annotate_background = Color('blue')
        camera.annotate_foreground = Color('yellow')
        camera.awb_mode = 'auto'
        dateNow = config['image']['date']
        camera.annotate_text = dateNow
        sleep(2)
        camera.capture('/home/pi/camera/public/utsikt_' + dateNow + '.jpg')
        camera.close()

# brightness()
# contrast()
# effects()
# dateNow = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

# sleep(3)
# print("In specified format:", dt_date.strftime("%Y-%m-%d_%H:%M:%S"))
# camera.start_recording('/home/pi/Desktop/video.h264')

# camera.stop_recording()
# camera.stop_preview()
