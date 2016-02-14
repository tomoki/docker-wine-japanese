# This is a fork from https://github.com/webanck/docker-wine-steam
This is a fork of great tools [docker-wine-stream] (https://github.com/webanck/docker-wine-steam) to adapt it Japanese games (mostly novel games)

The difference from original repo are following:
- Change locale to Japanese for character corruption (in Japanese, "文字化け")
- Install VLGothic as Japanese font
- a little tweak

#Windows (Japanese) games on Linux!

Play Japanese Windows games on Linux using Wine to do so and confining the mess inside a Docker container.
Bind X11's socket for the windows to appear and use ear the sound from PulseAudio.

##Prerequisites

###Docker

Be sure to have Docker installed. Detailed explanations are given on the [Docker official site](https://docs.docker.com/installation/).
For Ubuntu 14.04 you can install the latest version of Docker with the following command.
```
wget -qO- https://get.docker.com/ | sh
```

###PulseAudio

For the sound to work, you need the PulseAudio server.
You can check if it's installed and configured by launching a sample sound and looking for a pulseaudio process.
```
aplay /usr/share/sounds/alsa/Front_Center.wav && ps -A | grep pulseaudio
```

###A supported GPU
Currently, Nvidia cards should work out of the box whereas AMD and Intel Integrated chipsets may require some additional work (tweaking in [builder.sh](./builder.sh)). Let me know about your experimentations!

##Installation
Clone this repository to get the [Dockerfile](./Dockerfile) and the helper scripts to build and launch a corresponding container.
```
git clone https://github.com/tomoki/docker-wine-japanese.git
cd docker-wine-japanese
./builder.sh
./launcher.sh
```

Then you should be inside the container as the wine user. 
The last steps are an ultimate Wine configuration and the installation of Steam (which you can skip if you just want to use Wine for Windows games/applications).

*Warning*: leaving the container typing `exit` or using the keys `Ctrl+C` will destroy all it's data including your installed games and saves. 
You might want to copy some files into the [shared_directory](shared_directory) which is mounted in the home of the wine user. Some scripts are provided to help you [import](shared_directory/importSteam.sh) or [export](shared_directory/exportSteam.sh) quickly your steam installation.
```
finalize_installation
```
It will open the Wine configuration tool `winecfg`.
My advice: let Windows XP as default.
In the Audio tab, choose pulseaudio for each device.

![audio tab configuration](./winecfg-audio.png)

In the Graphics tab, I recommend to disable windows decorations and to emulate a virtual desktop of your screen's resolution.

![graphics tab configuration](./winecfg-graphics.png)

After the installation of Steam, you can simply use the provided alias `steam` to launch it.
Before playing any game, be sure to turn the Steam overlay off (uncheck Steam->Settings->In-Game->Enable the Steam Overlay) because it's not supported by Wine.

##Motivation
Have you ever tried to install Wine?
And have you ever tried to install Wine while using CUDA on your system?
Well, if you have not, do not try, it's messy.
