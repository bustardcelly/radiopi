# Requires pulling in https://github.com/adafruit/Adafruit_ILI9341
import Image
import cStringIO as io

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

DC = 24
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0

class TFTDisplay:
  def __init__(self):
    self.display = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000), gpio=None, width=128, height=128)
    self.display.begin()

  def show(self, byte_str):
    if byte_str is None:
      print "No Image Found"
      return
    stream = io.StringIO(byte_str)
    img = Image.open(stream)
    print "incoming image"
    print img.size
    self.display.begin()
    img.rotate(90).resize((128, 128), Image.ANTIALIAS)
    self.display.display(img)
