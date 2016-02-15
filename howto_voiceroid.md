# Install
Voiceroid is a proprietary software, so we need special procedures.
Here is overview:

1. Build the image which contains Wine 1.6 (1.7 or higher does not work well with voiceroid)
2.1. Make container which install voiceroid on top of the image.
2.2. Build image
3. Install image file
4. Enjoy voiceroid :)

## 1. Build the image
First, we need to create image. This takes a while (10 mins or so).
```{.sh}
git clone -b voiceroid https://github.com/tomoki/docker-wine-japanese.git
cd docker-wine-japanese
./builder.sh
```

## 2.1. Install Voiceroid to container
WARNING: please keep it running until we end up phase 2.2.
```{.sh}
./make_container.sh
# Install Voiceroid (i.e run voiceroid_yukari_dl.exe, or setup.exe)
# shared_directory can be used to share exe between host and cotnainer.
# i.e, in host,       $ cp voiceroid_yukari_dl.exe shared_directory
#      in container,  $ wine shared_directory voiceroid_yukari_dl.exe
# to run voiceroid,   $ wine start .wine/drive_c/users/wine/Desktop/VOICEROID＋\ 結月ゆかり.lnk
```

## 2.2 Build image
First, check container id, which we create at 2.1.
```{.sh}
sudo docker ps -a

CONTAINER ID IMAGE                   COMMAND                CREATED       STATUS      PORTS NAMES
24f120fb0db7 tomoki/docker-voiceroid "/bin/sh -c /bin/bash" 3 seconds ago Up 2 second       voiceroid_cont
```

In this case, `24f120fb0db7` is what we are looking for.
We generate image from the container to share between multiple physical machines.

WARNING: When creating image, we use UID.
It means that we cannot share image file where UID is different.
It sometime occurs when there are multiple users on physical machine.

```{.sh}
sudo docker export 24f120fb0db7 > voiceroid_docker_image.tar
```

## 3. Import image file

We can import in the other physical machine.
```{.sh}
cat voiceroid_docker_image.tar | sudo docker import - voiceroid-dock
```

Of course, we can run from its image.
```{.sh}
./launcher.sh
```

# 4. Run as a server
As a bonus, I included server script in [shared_directory](shared_directory).

```{.sh}
# in host
./launcher_with_port.sh

# in container
wine start .wine/drive_c/users/wine/Desktop/VOICEROID＋\ 結月ゆかり.lnk
python3 shared_directory/server.py

# in host
wget "http://localhost:48234?message=hello&speaker=yukari"
```
