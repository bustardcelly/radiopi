import sys
import usb.core
import usb.util

# find our device
devices = usb.core.find(find_all=True)

if devices is None:
  raise ValueError('Device is not connected')

for dev in devices:
  for cfg in dev:
    print "cfg value: %r" % str(cfg.bConfigurationValue)