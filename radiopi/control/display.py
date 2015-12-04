import serial
import time

import radiopi.settings as settings

from radiopi import prettyprint
from radiopi import COLORS

CLEAR = b'\xFE\x01'
WRITE = b'\xFE\x80'
OFF = b'\xFE\x41'
ON = b'\xFE\x42'

def split(text):
  return text.rsplit(settings.FILEDATA_DELIMITER)

def pad(text, max_length):
  text_length = len(text)
  if text_length < max_length:
    text = text.ljust(max_length, ' ')
  return text

class ConsoleDisplay():
  def __init__(self):
    self.context = None

  def show(self, text):
    if self.context != text:
      for line in split(text):
        prettyprint(COLORS.BLUE, line)
      self.context = text

class LCDDisplay():
  def __init__(self, columns, rows):
    print "LCDDisplay init()..."
    self.index = 0
    self.threshold = 0
    self.context = None
    self.lines = []
    self.vector = 1
    self.columns = columns
    self.rows = rows
    self.ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.1)
    self.ser.write(OFF)
    self.ser.write(ON)
    self.ser.write(WRITE)
    self.clear()
    time.sleep(2)

  def clear(self):
    self.index = 0
    self.vector = 1
    self.threshold = 0
    del self.lines[0:len(self.lines)]
    self.ser.write(CLEAR)

  def scroll(self):
    self.ser.write(WRITE)
    output = ''
    self.ser.write(self.lines[0][self.index:self.index+self.columns])
    if len(self.lines) > 1:
      self.ser.write(b'\xFE\xC0')
      self.ser.write(self.lines[1][self.index:self.index+self.columns])

  def scroll_right(self):
    self.vector = 1
    stable = self.index < self.threshold
    if stable:
      self.index = self.index + self.vector
      self.scroll()
    else:
      self.scroll_left()

  def scroll_left(self):
    self.vector = -1
    stable = self.index > 0
    if stable:
      self.index = self.index + self.vector
      self.scroll()
    else:
      self.scroll_right()

  def update(self):
    if self.vector == 1:
      self.scroll_right()
    else:
      self.scroll_left()

  def show(self, text):
    if self.context != text:
      self.clear()
      print "show: %s" % text
      split_rows = split(text)[:self.rows]
      longest_row = max(split_rows, key=len)
      longest_row_length = len(longest_row)
      longest_length = self.columns if longest_row_length < self.columns else longest_row_length
      self.threshold = longest_length - self.columns
      for row in split_rows:
        self.lines.append(pad(row, longest_length))
      self.context = text
      self.scroll()
    else:
      if self.threshold > 0:
        self.update()

