#!/bin/sh

CONTAINER_NAME=`cat /dev/urandom | tr -dc '[:alnum:]' | head -c 10`

echo 'Trying to run new data container.'
#The container will be destroyed when left to avoid volume mounting problems, especially the hold of the Xauthority and pulseaudio files by non destroyed Docker volumes causing OS and Docker failures after reboot.
sudo docker run -ti --rm \
		-e DISPLAY \
		-v /tmp/.X11-unix:/tmp/.X11-unix:ro \
		-v ~/.Xauthority:/home/wine/.Xauthority \
		-v /dev/snd:/dev/snd --privileged \
		-v /run/user/`id -u`/pulse/native:/run/user/`id -u`/pulse/native \
		-v /etc/localtime:/etc/localtime:ro \
		-v `pwd`/shared_directory:/home/wine/shared_directory \
		--net=host \
		--name $CONTAINER_NAME \
		--user wine \
		-e HOME=/home/wine \
		-e WINEPREFIX=/home/wine/.wine \
		-e WINEARCH=win32 \
		-e WINEDEBUG=-all \
		-e PULSE_SERVER=unix:/run/user/$UID/pulse/native \
		-e DEBIAN_FRONTEND=noninteractive \
		-e LANG=ja_JP.UTF-8 \
		-e LANGUAGE=ja_JP:ja \
		-e LC_ALL=ja_JP.UTF-8 \
		-w /home/wine \
		-p 12345:12345 \
		voiceroid-dock \
		/bin/sh -c /bin/bash
