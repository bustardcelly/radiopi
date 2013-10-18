import sys
# import usb.core
# import usb.util
import time
import pygame

from radiopi.player.broadcast import PyGameBroadcast
from radiopi.file.audiodir import AudioDirectory
from radiopi.model.session import Session
from radiopi.player.radio import Radio
from radiopi.control.dial import Dial

SONG_END = pygame.USEREVENT + 1

# find our device
# devices = usb.core.find(find_all=True)

# if devices is None:
#   raise ValueError('Device is not connected')

# for dev in devices:
#   for cfg in dev:
#     print "cfg value: %r" % str(cfg.bConfigurationValue)

def main():
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
      event = pygame.event.poll()
      if event.type == SONG_END:
        radio.station.next()
      '''
      if pot.input_value.changed:
        dial.set_value(pot.input_value)
      '''
      time.sleep(0.5)
    dial.set_value(0)

if __name__ == '__main__':
  main()
