#!/usr/bin/env bash
pushd 'pi-camera-ui'
# ng build
popd
rsync -a -v -L lib node_modules package.json package-lock.json proxy.js public pi_service_camera.py service_camera_config.py service_snap_if_diff.py utilities.py service_static.js pi@192.168.86.217:/home/pi/camera
