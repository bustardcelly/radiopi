import serial

import radiopi.settings as settings

from radiopi import prettyprint
from radiopi import COLORS

CLEAR = "x\0C"
WRITE = "\xfe\x01"
SCROLL_LEFT = "x18"
SCROLL_RIGHT = "x1C"

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
    self.index = 0
    self.threshold = 0
    self.context = None
    self.lines = []
    self.vector = 1
    self.columns = columns
    self.rows = rows
    self.ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.1)
    self.clear()

  def clear(self):
    self.index = 0
    self.vector = 1
    del self.lines[0:len(self.lines)]
    self.ser.write(CLEAR)

  def scroll(self):
    self.ser.write(WRITE)
    output = ''
    for line in self.lines:
      output += line[self.index:self.index+self.columns] 
    self.ser.write(output)

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
    if threshold > 0:
      if self.vector == 1:
        self.scroll_right()
      else:
        self.scroll_left()

  def show(self, text):
    if self.context != text:
      self.clear()
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
      update()

