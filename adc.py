from radiopi.control.mcp3008 import ADC
import time

if __name__ == '__main__':
  adc = ADC()
  adc.open()
  while True:
    try:
      print "%r" % adc.readadc(0)
      time.sleep(0.5)
    except KeyboardInterrupt:
      adc.close()
      sys.exit('\nExplicit close.')