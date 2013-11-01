# http://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/script

import os
import sys
# import usb.core
# import usb.util
import math
import time
import pygame
import argparse

from radiopi.player.broadcast import PyGameBroadcast
from radiopi.player.broadcast import OSXBroadcast
from radiopi.file.audiodir import AudioDirectory
from radiopi.model.session import Session
from radiopi.player.radio import Radio
from radiopi.control.dial import Dial
from radiopi.control.display import LCDDisplay

from radiopi import prettyprint
from radiopi import COLORS

import RPi.GPIO as GPIO
from datetime import datetime

SONG_END = pygame.USEREVENT + 1
STEP_INCREMENT = 100
PAUSE_LENGTH = 1 # in microseconds

# POT
GPIO.setmode(GPIO.BCM)
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

read_values = []
potentiometer_adc = 0
last_read = 0
tolerance = 5

# Dial
clock = 0
dial_value = 0.0
previous_dial_value = 0.0

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

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
  if ((adcnum > 7) or (adcnum < 0)):
    return -1

  GPIO.output(cspin, True)
  GPIO.output(clockpin, False)  # start clock low
  GPIO.output(cspin, False)     # bring CS low

  commandout = adcnum
  commandout |= 0x18  # start bit + single-ended bit
  commandout <<= 3    # we only need to send 5 bits here
  for i in range(5):
    if (commandout & 0x80):
      GPIO.output(mosipin, True)
    else:
      GPIO.output(mosipin, False)
    commandout <<= 1
    GPIO.output(clockpin, True)
    GPIO.output(clockpin, False)

  adcout = 0
  # read in one empty bit, one null bit and 10 ADC bits
  for i in range(12):
    GPIO.output(clockpin, True)
    GPIO.output(clockpin, False)
    adcout <<= 1
    if (GPIO.input(misopin)):
      adcout |= 0x1

  GPIO.output(cspin, True)
  
  adcout >>= 1       # first bit is 'null' so drop it
  return adcout

def setup_peripherals():
  GPIO.cleanup()
  GPIO.setup(SPIMOSI, GPIO.OUT)
  GPIO.setup(SPIMISO, GPIO.IN)
  GPIO.setup(SPICLK, GPIO.OUT)
  GPIO.setup(SPICS, GPIO.OUT)

def get_average(value):
  global read_values
  read_values.append(value)
  if len(read_values) > 10:
    read_values.pop(0)
  return math.fsum(read_values) / float(len(read_values))

def check_dial():
  global potentiometer_adc
  global last_read
  global tolerance
  global dial_value
  global clock

  # read the analog pin
  trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
  prettyprint(COLORS.YELLOW, 'trim: %f' % trim_pot)
  # how much has it changed since the last read?
  pot_adjust = abs(trim_pot - last_read)
  if pot_adjust > tolerance:
    dial_value = (trim_pot / 10.24) / 100   # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
    prettyprint(COLORS.WHITE, 'POT ADJESTED %f' % dial_value)
    # save the potentiometer reading for the next loop
    last_read = trim_pot
    clock = datetime.now()

def pi_main():
  global clock
  global dial_value
  global previous_dial_value

  # TODO: Mount USB

  display = LCDDisplay(16, 2)
  display.show('parsing...')

  session = Session()
  session.inflate(AudioDirectory('/mnt/usb/AUDIO').parse())

  player = PyGameBroadcast()
  player.listen_on(SONG_END)
  
  radio = Radio(session, player)

  dial = Dial()
  dial.range(session.start_year(), session.end_year())
  dial.add_listener(radio.dial_change_delegate)

  # session.print_listing()
  dial.set_value(dial_value)
  running = True

  while running:
    try:
      check_dial()
      if player.playing:
        event = player.poll()
        if event.type == SONG_END:
          prettyprint(COLORS.WHITE, 'Song end: radio.station.next()')
          radio.station.next()
        # prettyprint(COLORS.YELLOW, 'Previous, %f, now, %f' % (previous_dial_value, dial_value))
        if previous_dial_value != dial_value:
          prettyprint(COLORS.YELLOW, 'difference: %d' % (datetime.now() - clock).seconds)
          if (datetime.now() - clock).seconds >= PAUSE_LENGTH:
            prettyprint(COLORS.BLUE, 'Dial change, value: %f ' % dial_value)
            previous_dial_value = dial_value
            prettyprint(COLORS.WHITE, 'YEAR: %s' + dial.set_value(dial_value))
          else:
            dial.set_roaming()
        display.show(radio.station.current())
      time.sleep(0.5)
    except KeyboardInterrupt:
      player.stop()
      running = false
      sys.exit('\nExplicit close.')

if __name__ == '__main__':
  unpack = Unpack()
  args = parser.parse_args(namespace=unpack)
  if args.environment == 'pi':
    setup_peripherals()
    pi_main()
