#!/usr/bin/env bash
rsync -a -v -L lib node_modules package.json package-lock.json proxy.js public pi_service_camera.py service_camera_config.py utilities.py service_static.js pi@192.168.86.175:/home/pi/camera
