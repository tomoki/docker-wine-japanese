#!/bin/sh

# Getting the user id.
if [ -z "$UID" ]; then
    UID=`id -u`
fi

# Copying the Dockerfile to set parameters.
cp -f Dockerfile /tmp/

# Setting the right user id.
sed -i -e "s/1001/$UID/g" /tmp/Dockerfile

# Building the image.
sudo docker build -t tomoki/docker-voiceroid /tmp/ 

# Cleaning up.
rm /tmp/Dockerfile
