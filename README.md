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
* [Pygame](http://www.pygame.org/download.shtml)

Optionally, [pygame from source](http://pygame.org/wiki/MacCompile)

And additional `brew` installs: [https://bitbucket.org/pygame/pygame/issues/82/homebrew-on-leopard-fails-to-install#comment-627494](https://bitbucket.org/pygame/pygame/issues/82/homebrew-on-leopard-fails-to-install#comment-627494)

Or, from this thread [https://www.reddit.com/r/pygame/comments/2l262j/pygame_on_mac_os_x_1010/](https://www.reddit.com/r/pygame/comments/2l262j/pygame_on_mac_os_x_1010/).

How I Resolved OSX
---

```
$ brew tap samueljohn/python
$ brew install pygame
$ mkdir pygame
$ cp -r /usr/local/Cellar/pygame/1.9.2a0/lib/python2.7/site-packages/pygame/* pygame/
```