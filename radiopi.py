# http://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/script

import os
import sys
# import usb.core
# import usb.util
import math
import time
import pygame
import argparse
import threading

from radiopi.player.broadcast import PyGameBroadcast
from radiopi.player.broadcast import OSXBroadcast
from radiopi.file.audiodir import AudioDirectory
from radiopi.model.session import Session
from radiopi.player.radio import Radio
from radiopi.control.dial import Dial
from radiopi.control.shifter import Shifter
from radiopi.control.display import LCDDisplay
from radiopi.control.year_display import FourSeven

from radiopi.control.mcp3008 import ADC

from radiopi import prettyprint
from radiopi import COLORS

import RPi.GPIO as GPIO
from datetime import datetime

SONG_END = pygame.USEREVENT + 1
STEP_INCREMENT = 100
PAUSE_LENGTH = 50000 # in microseconds

# POT
GPIO.setmode(GPIO.BCM)
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# 4x7 Segment
DATA_PIN = 17
CLOCK_PIN = 22
LATCH_PIN = 18
REGISTER_COUNT = 2

# adc
adc = None
read_values = []
potentiometer_adc = 0
trim_pot = 0
trim_alpha = 2
trim_beta = 3
trim_expo = 2
variance_count = 0
variance_limit = 3
last_read = 0
tolerance = 5
avg_alpha = 0.7

# Dial
clock = 0
dial_value = 0.0
previous_dial_value = 0.0

# Parse options
parser = argparse.ArgumentParser(description="Ra-dio player.")
parser.add_argument('-en', '--environment', default='pi', type=str, \
  help='Provide the environment to run under.')

class Unpack(object):
  pass

class YearDisplayThread(threading.Thread):
  """ Thread to print year value based on dial input. """
  def __init__(self, display, dial):
    self.display = display
    self.dial = dial
    threading.Thread.__init__(self)

  def run(self):
    while True:
      self.display.show_number(self.dial.input_value)

class LCDDisplayThread(threading.Thread):
  """ Thread to print song metadata based on selected radio station. """
  def __init__(self, display, radio):
    self.display = display
    self.radio = radio
    threading.Thread.__init__(self)

  def run(self):
    while True:
      self.display.show(self.radio.station.current())
      time.sleep(0.5)

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

def get_weighted_smooth(value):
  global trim_pot
  global trim_alpha
  global trim_beta
  return (value * trim_alpha + trim_pot * trim_beta) / (trim_alpha + trim_beta)

def get_exponential_smooth(value):
  global trim_pot
  return trim_pot + (value - trim_pot) >> trim_expo

def check_dial():
  global adc
  global potentiometer_adc
  global trim_pot
  global variance_count
  global variance_limit
  global last_read
  global tolerance
  global dial_value
  global clock

  # read the analog pin
  # trim_pot = get_average(readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS))
  # trim_pot = get_weighted_smooth(readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS))
  # trim_pot = get_exponential_smooth(readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS))
  # trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
  trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
  # how much has it changed since the last read?
  pot_adjust = abs(trim_pot - last_read)
  if pot_adjust > tolerance:
    variance_count += 1
    if variance_count >= variance_limit:
      variance_count = 0
      dial_value = (trim_pot / 10.24) / 100   # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
      prettyprint(COLORS.WHITE, 'POT ADJESTED. trim: %f, dial: %f' % (trim_pot, dial_value))
      # save the potentiometer reading for the next loop
      last_read = trim_pot
      clock = datetime.now()
  else:
    variance_count = 0 if variance_count == 0 else variance_count - 1

def pi_main():
  global adc
  global clock
  global dial_value
  global previous_dial_value

  # TODO: Auto Mount USB
  
  display = LCDDisplay(16, 2)
  display.show('parsing...')

  shifter = Shifter(DATA_PIN, CLOCK_PIN, LATCH_PIN)
  shifter.set_shift_register_count(REGISTER_COUNT)

  year_display = FourSeven(shifter)
  year_display.show_passive()

  session = Session()
  session.inflate(AudioDirectory('/mnt/usb/hip hop').parse())

  player = PyGameBroadcast()
  player.listen_on(SONG_END)
  
  radio = Radio(session, player)

  dial = Dial()
  dial.range(session.start_year(), session.end_year())
  dial.add_listener(radio.dial_change_delegate)

  adc = ADC()
  adc.open()

  # session.print_listing()
  dial.set_value(dial_value)
  running = True
  year = -1

  # threads
  lcdThread = LCDDisplayThread(display, radio)
  yearThread = YearDisplayThread(year_display, dial)
  lcdThread.setDaemon(True)
  yearThread.setDaemon(True)
  lcdThread.start()
  yearThread.start()

  while running:
    try:
      check_dial()
      if player.playing:
        event = player.poll()
        if event.type == SONG_END:
          prettyprint(COLORS.WHITE, 'Song end: radio.station.next()')
          radio.station.next()
        if previous_dial_value != dial_value:
          if (datetime.now() - clock).microseconds >= PAUSE_LENGTH:
            year = dial.set_value(dial_value)
            prettyprint(COLORS.BLUE, 'YEAR: %d' % year)
            previous_dial_value = dial_value
          else:
            year = dial.set_roaming()
            prettyprint(COLORS.BLUE, 'YEAR: ----')
      time.sleep(0.3)
    except KeyboardInterrupt:
      player.stop()
      adc.close()
      running = false
      sys.exit('\nExplicit close.')

if __name__ == '__main__':
  unpack = Unpack()
  args = parser.parse_args(namespace=unpack)
  if args.environment == 'pi':
    setup_peripherals()
    pi_main()
