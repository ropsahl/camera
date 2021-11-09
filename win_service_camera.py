import datetime

import sys

from lib.bottle import run, post, error, request, route
from utilities import port


class PiCamera():
    def __init__(self):
        self.rotation = 0

    def __enter__(self):
        print('Entered')
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        print('Exited')

@route('/live')
def live():
    return "live and kicking"


@post('/snap')
def snap():
    config = request.json
    print(config)
    with PiCamera() as camera:
        if 'image' in config:
            if 'rotation' in config['image']:
                camera.rotation = config['image']['rotation']
            if 'width' in config['image'] and 'height' in config['image']:
                camera.resolution = (config['image']['width'], config['image']['height'])
        if 'config' in config:
            if 'effects' in config['config']:
                camera.image_effect = config['config']['effects']
            if 'contrast' in config['config']:
                camera.contrast = config['config']['contrast']
            if 'brightness' in config['config']:
                camera.brightness = config['config']['brightness']
            if 'exposure' in config['config']:
                camera.exposure_mode = config['config']['exposure']
        date_now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        camera.annotate_text = date_now
        file_name = 'utsikt_' + date_now + '.jpg'
    return '{"file_name": "' + file_name + '"}'


@error(404)
def err_404(error):
    print(error)
    return 'Sorry ' + str(error)


@error(500)
def err_500(error):
    print(error)
    return 'Sorry ' + str(error)


print('----------- ' + sys.argv[0] + " starting on port: " + str(port(sys.argv[0], 8210)))
run(host='localhost', port=port(sys.argv[0], 8210), debug=True)
