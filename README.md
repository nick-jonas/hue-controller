# Hue Controller for the Raspberry Pi

These files are meant to placed in /home/pi/hue/ on the RPi.


# Necessary packages for the Linux Image

## Update python (2.x) to the latest release.

```
sudo apt-get install python-dev
```

## Install the latest RPi.GPIO module (0.3.1a). We will use easy_install to manage the python packages. 

```
sudo apt-get install python-setuptools
sudo easy_install rpi.gpio
```

## Install Phue

```
sudo easy_install phue
```

*or*

```
sudo apt-get install python-pip
pip install phue
```


# Systemd Installation

This uses systemd for initializing for speed (over init.d).  

First install system.d:

```
$ apt-get install systemd
```

Then tell the kernel to use systemd as the init system, by appending ```init=/bin/systemd``` to the end of ```/boot/cmdline.txt``` line.  Example:

```
dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait init=/bin/systemd
```

To list available units: ```systemctl```


## Create Hue init service

Create ```hue.service``` in ```/etc/systemd/system/``` and paste this into it:

```
[Unit]
Description=Hue Controller
Requires=local-fs.target
After=local-fs.target

[Service]
Type=forking
ExecStart=/home/pi/hue/bin/hue.sh

[Install]
WantedBy=multi-user.target
```

Then make systemd aware of the service:

```
systemctl daemon-reload
systemctl enable myFancy.service
systemctl start myFancy.service
```

