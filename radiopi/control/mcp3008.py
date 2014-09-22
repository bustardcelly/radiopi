# https://github.com/jerbly/tutorials/blob/master/moisture/mcp3008.py

import spidev

class ADC():
    def __init__(self):
        self.spi = spidev.SpiDev()

    def open(self):
        self.spi.open(0,1)

    def close(self):
        self.spi.close()

    # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    def readadc(self, adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        r = self.spi.xfer2([1,(8+adcnum)<<4,0])
        adcout = ((r[1]&3) << 8) + r[2]
        return adcout

    def read_pct(self, adcnum):
        r = self.readadc(adcnum)
        return int(round((r/1023.0)*100))

    def read_3v3(self, adcnum):
        r = self.readadc(adcnum)
        v = (r/1023.0)*3.3
        return v

    def readadc_avg(self, adcnum):
        r = []
        for i in range (0,10):
            r.append(self.readadc(adcnum))
        return sum(r)/10.0