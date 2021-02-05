import datetime
import json
import os

import requests
import sys
from builtins import print

from lib.bottle import static_file, route, run, get, post, request
from utilities import port, router_host

print("Running on " + os.name)
for key in os.environ.keys():
    print(key + ": " + os.getenv(key))
if os.name == 'nt' or os.getenv("HOSTTYPE") == "x86_64":
    pass  # Windows
else:
    pass

METER_MODES = (
    'average',
    'spot',
    'backlit',
    'matrix'
)

EXPOSURE_MODES = (
    'off',
    'auto',
    'night',
    'nightpreview',
    'backlight',
    'spotlight',
    'sports',
    'snow',
    'beach',
    'verylong',
    'fixedfps',
    'antishake',
    'fireworks',
)

FLASH_MODES = (
    'off',
    'auto',
    'on',
    'redeye',
    'fillin',
    'torch',
)

AWB_MODES = (
    'off',
    'auto',
    'sunlight',
    'cloudy',
    'shade',
    'tungsten',
    'fluorescent',
    'incandescent',
    'flash',
    'horizon'
)

IMAGE_EFFECTS = (
    'none',
    'negative',
    'solarize',
    # The following don't work
    # 'posterize',
    # 'whiteboard',
    # 'blackboard',
    'sketch',
    'denoise',
    'emboss',
    'oilpaint',
    'hatch',
    'gpen',
    'pastel',
    'watercolor',
    'film',
    'blur',
    'saturation',
    'colorswap',
    'washedout',
    'posterise',
    'colorpoint',
    'colorbalance',
    'cartoon',
    'deinterlace1',
    'deinterlace2'
)

DRC_STRENGTHS = (
    'off',
    'low',
    'medium',
    'high'
)

RAW_FORMATS = (
    'yuv',
    'rgb',
    'rgba',
    'bgr',
    'bgra'
)

STEREO_MODES = (
    'none',
    'side-by-side',
    'top-bottom'
)

CLOCK_MODES = (
    'reset',
    'raw'
)

configProperties = {
    "meter": METER_MODES,
    "exposure": EXPOSURE_MODES,
    "flash": FLASH_MODES,
    "awb": AWB_MODES,
    "imageEffects": IMAGE_EFFECTS,
    "drcStrengths": DRC_STRENGTHS,
    "rawFormats": RAW_FORMATS,
    "stereo": STEREO_MODES,
    "clock": CLOCK_MODES
}


@route('/hello')
@route('/')
def hello():
    return "<html><body>" \
           "<h1>Config server</h1><p>My endpoints are:</p>" \
           "<a href='/camera_config/config'>Test endpoint: GET /camera_config/config </a>" \
           "</body></html>"


@get('/config/<property>')
def get_config_property(property):
    print('/config/' + property)
    if property in configProperties:
        return json.dumps(configProperties[property])

    ret = []
    for k in configProperties.keys():
        ret.append(k)
    return json.dumps(ret)


@get('/config')
def get_config_properties():
    print('/config/')
    ret = []
    for k in configProperties.keys():
        ret.append(k)
    return json.dumps(ret)


@get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='C:/Users/runar/projects/pi/camera')


@get('/config/current')
def get_current_config():
    return merge({})


@post('/camera')
def configure():
    print('/camera')
    adjustments = request.json
    merged_config = merge(adjustments)
    print(merged_config)
    url = camera_url()
    merged_config['image']['date'] = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    print('POST: ' + url)
    response = requests.post(url, json=merged_config)
    if response.ok:
        print('file_name' + str(response.json()))
        merged_config['image']['fileName'] = response.json()['file_name']
        return merged_config


def merge(adjustments):
    with open("cameraConfig.json", "r") as current_config:
        camera_config = json.load(current_config)
        for camera_element in camera_config:
            if camera_element in adjustments.keys():
                for prop in camera_config[camera_element]:
                    if prop in adjustments[camera_element].keys():
                        camera_config[camera_element][prop] = adjustments[camera_element][prop]

    with open("cameraConfig.json", "w") as mergedConfig:
        mergedConfig.write(json.dumps(camera_config, indent=2))
    return camera_config


def camera_url():
    router = router_host(sys.argv[0])
    if router is not None:
        return router + '/camera/snap'
    return 'http://localhost:8210/snap'


run(host='localhost', port=port(sys.argv[0], 8200), debug=True)
