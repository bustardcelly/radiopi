Setup
---
Pull down repo on Raspberry Pi (used Raspbien Wheezy).

Create virtual environment and resolve dependencies

```
$ mkvirtualenv ra-dio -r requirements.txt --system-site-packages
```

Create a mount directory

```
$ sudo mkdir /mnt/usb
```

Insert and Search for mounted usb drive

```
$ ls /dev/ | grep sd
```

Mount the usb drive

```
$ sudo mount /dev/sda2 /mnt/usb
```

Run
---
```
$ workon ra-dio
$ sudo python radiopi.py
```

Requirements
---

##OSX

* [X11](http://xquartz.macosforge.org/landing/)
* [Pygame](http://www.pygame.org/download.shtml)a

Optionally, [pygame from source](http://pygame.org/wiki/MacCompile)

And additional `brew` installs: [https://bitbucket.org/pygame/pygame/issues/82/homebrew-on-leopard-fails-to-install#comment-627494](https://bitbucket.org/pygame/pygame/issues/82/homebrew-on-leopard-fails-to-install#comment-627494)