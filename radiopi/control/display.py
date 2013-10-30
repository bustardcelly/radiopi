import serial

import radiopi.settings as settings

from radiopi import prettyprint
from radiopi import COLORS

def split(text):
  return text.rsplit(settings.FILEDATA_DELIMITER)

class ConsoleDisplay():
  def __init__(self):
    self.context = None
    pass

  def show(self, text):
    if self.context != text:
      for line in split(text):
        prettyprint(COLORS.BLUE, line)
      self.context = text

class LCDDisplay():
  def __init__(self):
    self.context = None
    self.ser = serial.Serial('/dev/ttyAMA0',9600,timeout=0.1)
    self.ser.write("x\0C")

  def show(self, text):
    if self.context != text:
      lines = split(text)
      for line in split(text):
        prettyprint(COLORS.BLUE, line)
      self.context = text

