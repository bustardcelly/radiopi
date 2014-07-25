import RPi.GPIO as GPIO
from time import sleep

class FourSeven:
  """
  Default Pins:

  Type      Seg Pin   Reg Pin
  ----      -------   -------
  Digit 1   1 pin     9 pin
  Digit 2   2 pin     10 pin
  Digit 3   6 pin     11 pin
  Digit 4   8 pin     12 pin
  Seg A     14 pin    1 pin
  Seg B     16 pin    2 pin
  Seg C     13 pin    3 pin
  Seg D     3 pin     4 pin
  Seg E     5 pin     5 pin
  Seg F     11 pin    6 pin
  Seg G     15 pin    7 pin

  Defines values are all "off by one" to be inserted into range starting at 0.
  """
  DIGIT_ONE = 8
  DIGIT_TWO = 9
  DIGIT_THREE = 10
  DIGIT_FOUR = 11

  SEG_A = 0
  SEG_B = 1
  SEG_C = 2
  SEG_D = 3
  SEG_E = 4
  SEG_F = 5
  SEG_G = 6

  digits = [DIGIT_ONE, DIGIT_TWO, DIGIT_THREE, DIGIT_FOUR]

  def __init__(self, shifter):
    self.shifter = shifter

  def show_number(self, number):
    self.clear()
    digit = 3
    while digit > -1:
      # for value in FourSeven.digits:
      #   self.shifter.set_pin(value, GPIO.LOW)
      # self.shifter.write()
      self.light_number(number % 10)
      self.shifter.set_pin(FourSeven.digits[digit], GPIO.HIGH)
      self.shifter.write()
      self.shifter.set_pin(FourSeven.digits[digit], GPIO.LOW)
      self.light_number(10)
      digit = digit - 1
      number = number / 10

  def show_passive(self):
    digit = 3
    while digit > -1:
      self.light_dash()
      self.shifter.set_pin(FourSeven.digits[digit], GPIO.HIGH)
      self.shifter.write()
      for value in FourSeven.digits:
        self.shifter.set_pin(value, GPIO.LOW)
      self.shifter.write()
      digit = digit - 1

  def clear(self):
    digit = 3
    while digit > -1:
      self.light_number(10)
      self.shifter.set_pin(FourSeven.digits[digit], GPIO.HIGH)
      for value in FourSeven.digits:
        self.shifter.set_pin(value, GPIO.LOW)
      self.shifter.write()
      digit = digit - 1

  def light_number(self, number):
    if number == 0:
      self.shifter.set_pin(FourSeven.SEG_A, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_B, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_C, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_D, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_E, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_F, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_G, GPIO.HIGH)
    elif number == 1:
      self.shifter.set_pin(FourSeven.SEG_A, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_B, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_C, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_D, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_E, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_F, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_G, GPIO.HIGH)
    elif number == 2:
      self.shifter.set_pin(FourSeven.SEG_A, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_B, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_C, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_D, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_E, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_F, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_G, GPIO.LOW)
    elif number == 3:
      self.shifter.set_pin(FourSeven.SEG_A, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_B, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_C, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_D, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_E, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_F, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_G, GPIO.LOW)
    elif number == 4:
      self.shifter.set_pin(FourSeven.SEG_A, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_B, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_C, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_D, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_E, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_F, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_G, GPIO.LOW)
    elif number == 5:
      self.shifter.set_pin(FourSeven.SEG_A, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_B, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_C, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_D, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_E, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_F, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_G, GPIO.LOW)
    elif number == 6:
      self.shifter.set_pin(FourSeven.SEG_A, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_B, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_C, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_D, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_E, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_F, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_G, GPIO.LOW)
    elif number == 7:
      self.shifter.set_pin(FourSeven.SEG_A, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_B, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_C, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_D, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_E, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_F, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_G, GPIO.HIGH)
    elif number == 8:
      self.shifter.set_pin(FourSeven.SEG_A, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_B, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_C, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_D, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_E, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_F, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_G, GPIO.LOW)
    elif number == 9:
      self.shifter.set_pin(FourSeven.SEG_A, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_B, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_C, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_D, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_E, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_F, GPIO.LOW)
      self.shifter.set_pin(FourSeven.SEG_G, GPIO.LOW)
    elif number == 10:
      self.shifter.set_pin(FourSeven.SEG_A, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_B, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_C, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_D, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_E, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_F, GPIO.HIGH)
      self.shifter.set_pin(FourSeven.SEG_G, GPIO.HIGH)

  def light_dash(self):
    self.shifter.set_pin(FourSeven.SEG_A, GPIO.HIGH)
    self.shifter.set_pin(FourSeven.SEG_B, GPIO.HIGH)
    self.shifter.set_pin(FourSeven.SEG_C, GPIO.HIGH)
    self.shifter.set_pin(FourSeven.SEG_D, GPIO.HIGH)
    self.shifter.set_pin(FourSeven.SEG_E, GPIO.HIGH)
    self.shifter.set_pin(FourSeven.SEG_F, GPIO.HIGH)
    self.shifter.set_pin(FourSeven.SEG_G, GPIO.LOW)
