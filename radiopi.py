import os
import sys
# import usb.core
# import usb.util
import time
import pygame
import argparse

from radiopi.player.broadcast import PyGameBroadcast
from radiopi.player.broadcast import OSXBroadcast
from radiopi.file.audiodir import AudioDirectory
from radiopi.model.session import Session
from radiopi.player.radio import Radio
from radiopi.control.dial import Dial

from radiopi import prettyprint
from radiopi import COLORS

SONG_END = pygame.USEREVENT + 1

class Unpack(object):
  pass

parser = argparse.ArgumentParser(description="Ra-dio player.")
parser.add_argument('-en', '--environment', default='pi', type=str, \
  help='Provide the environment to run under.')

# find our device
# devices = usb.core.find(find_all=True)

# if devices is None:
#   raise ValueError('Device is not connected')

# for dev in devices:
#   for cfg in dev:
#     print "cfg value: %r" % str(cfg.bConfigurationValue)

def pi_main():
  # TODO: Mount USB
  session = Session()
  session.inflate(AudioDirectory('/mnt/usb/AUDIO').parse())

  player = PyGameBroadcast()
  player.listen_on(SONG_END)
  
  radio = Radio(session, player)

  dial = Dial()
  dial.range(session.start_year(), session.end_year())
  dial.add_listener(radio.dial_change_delegate)

  session.print_listing()

  while True:
    while player.playing:
      event = player.poll()
      if event.type == SONG_END:
        radio.station.next()
      '''
      if pot.input_value.changed:
        dial.set_value(pot.input_value)
      '''
      time.sleep(0.5)
    dial.set_value(0)

if __name__ == '__main__':
  unpack = Unpack()
  args = parser.parse_args(namespace=unpack)
  if args.environment == 'pi':
    pi_main()
