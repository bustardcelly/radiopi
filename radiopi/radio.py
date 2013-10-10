import sys
import usb.core
import usb.util
import time
import pygame

SONG_END = pygame.USEREVENT + 1

# find our device
devices = usb.core.find(find_all=True)

if devices is None:
  raise ValueError('Device is not connected')

for dev in devices:
  for cfg in dev:
    print "cfg value: %r" % str(cfg.bConfigurationValue)

def main():
  session = Session()
  session.inflate(AudioDirectory('/mnt/usb'))

  player = PyGameBroadcast()
  player.listen_on(SONG_END)
  
  radio = Radio(session, player)

  dial = Dial()
  dial.range(session.start_year, end_year)
  dial.add_listener(radio.dial_change_delegate)

  while True:
    event = pygame.event.poll()
    if event.type == SONG_END:
      radio.station.next()
    '''
    if pot.input_value.changed:
      dial.set_value(pot.input_value)
    '''
    time.wait(0.5)
