Setup
---
Create virtual environment and resolve dependencies

```
mkvirtualenv ra-dio -r requirements.txt --system-site-packages
```

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

SPI
---
SPI used for ADC of mcp3008 chip: [http://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/](http://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/)


Run
---
```
sudo python radiopi.py
```