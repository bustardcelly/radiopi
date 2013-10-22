import os
import sys
import time
import pygame
import argparse

from radiopi.player.broadcast import PyGameBroadcast
from radiopi.player.broadcast import OSXBroadcast
from radiopi.file.audiodir import AudioDirectory
from radiopi.model.session import Session
from radiopi.player.radio import Radio
from radiopi.control.dial import Dial

from radiopi import prettyprint
from radiopi import COLORS

from Tkinter import *

SONG_END = pygame.USEREVENT + 1
STEP_INCREMENT = 100

root = Tk()
frame = Frame(root, width=100, height=100)

dial_position = 0.0
previous_dial = -1.0
session = Session()
# session.inflate(AudioDirectory(os.path.abspath('./features/fixtures/audio')).parse())
session.inflate(AudioDirectory(os.path.abspath('/Users/toddanderson/Music/hip hop')).parse())

player = OSXBroadcast()
player.listen_on(SONG_END)

radio = Radio(session, player)

dial = Dial()
dial.range(session.start_year(), session.end_year())
dial.add_listener(radio.dial_change_delegate)

# session.print_listing()
session.print_uncategorized()

def limit_dial(step):
  global dial_position
  dial_position = dial_position + (step/STEP_INCREMENT)
  dial_position = 1 if dial_position > 1 else dial_position
  dial_position = 0 if dial_position < 0 else dial_position

def keypress(event):
  if event.keysym == 'Up':
    limit_dial(1.0)
  elif event.keysym == 'Down':
    limit_dial(-1.0)
 
def handler(event=None):
  global player
  global dial
  global radio
  global previous_dial
  global dial_position
  try:
    if player.playing:
      event = player.poll()
      if event.type == SONG_END:
        prettyprint(COLORS.WHITE, 'Song end: radio.station.next()')
        radio.station.next()
      time.sleep(0.5)
    if previous_dial != dial_position:
      prettyprint(COLORS.BLUE, 'Dial change, value: %f ' % dial_position)
      previous_dial = dial_position
      dial.set_value(dial_position)
  except KeyboardInterrupt:
    player.stop()
    sys.exit('\nExplicit close.')
  root.after(200, handler)

if __name__ == '__main__':
  frame.bind_all('<Key>', keypress)
  frame.pack()
  root.after(200, handler)
  root.mainloop()
