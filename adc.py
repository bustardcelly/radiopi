from radiopi.control.mcp3008 import ADC
from radiopi.control.mcp3008 import ADC2
import RPi.GPIO as GPIO
import time

if __name__ == '__main__':
  GPIO.setmode(GPIO.BCM)
  adc = ADC2()
  adc.open()
  while True:
    try:
      print "%r" % adc.readadc(0)
      time.sleep(0.5)
    except KeyboardInterrupt:
      adc.close()
      sys.exit('\nExplicit close.')