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


Run
---
```
sudo python radiopi.py
```