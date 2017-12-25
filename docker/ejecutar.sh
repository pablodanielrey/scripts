#!/bin/bash
sudo docker run -ti --rm --name scripts --env-file $HOME/gitlab/fce/produccion/scripts \
	-p 9090:5000 \
	-v $(pwd)/src:/src \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-v $(pwd)/android/home:/home/developer \
	--privileged \
	-v /dev/bus/usb:/dev/bus/usb \
	scripts bash

