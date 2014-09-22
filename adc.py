from radiopi.control.mcp3008 import ADC

if __name__ == '__main__':
  adc = ADC()
  while True:
    try:
      adc.readadc(0)
      time.sleep(0.5)
    except KeyboardInterrupt:
      adc.close()
      sys.exit('\nExplicit close.')