#!/bin/sh

CONTAINER_NAME=voiceroid_cont

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
		tomoki/docker-voiceroid \
|| \
echo 'Container already exists, it need to be erased.'
