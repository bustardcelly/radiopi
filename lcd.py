import argparse
from radiopi.control.display import LCDDisplay

class Unpack(object):
  pass

parser = argparse.ArgumentParser(description="LCD Display using TTY serial.")
parser.add_argument('-t', '--text', default='hello, world', type=str, help='Provide the environment to run under.')

if __name__ == '__main__':
  unpack = Unpack()
  args = parser.parse_args(namespace=unpack)
  display = LCDDisplay(16, 2)
  display.clear()
  print "print: %s" % args.text
  display.show(args.text)
