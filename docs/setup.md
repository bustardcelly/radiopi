SD Image
===
* Used Raspbian image: [http://www.raspberrypi.org/downloads](http://www.raspberrypi.org/downloads)
* Installed using [Raspberry-Pi-SD-Installer](http://learn.adafruit.com/adafruit-raspberry-pi-lesson-1-preparing-and-sd-card-for-your-raspberry-pi/making-an-sd-card-using-a-mac)

WiFi
===
* Used Edimax: [http://elinux.org/RPi_edimax_EW-7811Un](http://elinux.org/RPi_edimax_EW-7811Un)

### Find Used Ports
---

* Work: _connected to PlayBrassMonkey_ __pi@10.1.10.24__
* Work: _connected to ir5_ __pi@192.168.0.59__
* Home: _connected to antwerp_, __pi@10.0.1.13__

### Locate connection of Pi.
---

1. Connect Pi to ethernet.
2. Supply power to Pi.
3. Open *Angry IP Scanner*
4. enter in _from_ __10.0.x.0__ _to_ __10.0.x.y__
5. Check each:

	```
	ssh pi@10.0.x.y
	```
6. Once connected:

	```
	sudo apt-get update
	sudo apt-get upgrade
	sudo shutdown -h now
	```
7. Plug in WiFi dongle.
8. Power up Pi.
9. Install [VNC on Pi](http://learn.adafruit.com/adafruit-raspberry-pi-lesson-7-remote-control-with-vnc/installing-vnc): 

	```
	sudo apt-get install tightvncserver
	vncserver :1
	```
10. Open Google VPN application
11. Enter: 10.0.1.13:1
12. Enter password on prompt.
13. Set up [WiFi visually](http://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup/setting-up-wifi-with-raspbian)
14. Shutdown, remove ethernet cable, power up Pi again.
15. Open *Angry IP Scanner* again - IP may have changed. (eg, home when from __10.0.1.0__ to __10.0.1.254__)
16. Connect:
	
	```
	ssh pi@10.0.x.y
	```
	
### Virtual Environment
---
First, install python-setuptools to allow for easy_install and/or pip:

```
sudo apt-get install python-setuptools
```

Install virtualenv and virtualenvwrapper:

```
sudo easy_install virtualenv
sudo easy_install pip
sudo pip install virtualenvwrapper
```

Setup bash paths: (Shell Startup File)

[http://virtualenvwrapper.readthedocs.org/en/latest/install.html](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)

### Install Git
---
```
sudo apt-get install git-core
```
### Pull radiopi
---
[Generate SSH key](https://help.github.com/articles/generating-ssh-keys): 

```
ssh-keygen -t rsa -C "<email>"
```

Clone to _~/radiopi_

```
git clone git@github.com:bustardcelly/radiopi.git radiopi
```

Setup virtualenv

```
cd radiopi
sudo mkvirtualenv ra-dio -r requirements.txt --system-site-packages
```

### Install external dependencies
---
#### PySerial
```
wget https://pypi.python.org/packages/source/p/pyserial/pyserial-2.7.tar.gz#md5=794506184df83ef2290de0d18803dd11
tar -xzf pyserial-2.7.tar.gz
cd pyserial-2.7/
sudo ~/.virtualenvs/ra-dio/bin/python setup.py install
```

### Mount external USB
---
Create a mount directory

```
sudo mkdir /mnt/usb
```

Insert and Search for mounted usb drive

```
ls /dev/ | grep sd
```

Mount the usb drive

```
sudo mount /dev/sda2 /mnt/usb
```

### Run
---
```
sudo ~/.virtualenvs/ra-dio/bin/python radiopi.py 
```
