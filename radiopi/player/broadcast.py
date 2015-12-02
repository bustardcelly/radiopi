import os
import sys
import pygame
import traceback
from subprocess import Popen as call
from threading import Timer

from radiopi import prettyprint
from radiopi import COLORS

class PyGameBroadcast():
  def __init__(self):
    # Using pygame without graphics/video
    # http://stackoverflow.com/questions/10220104/pygame-error-video-system-not-initialized-on-ubuntu-server-with-only-terminal
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    try:
      pygame.init()
      self.playing = False
      print 'Pygame Broadcast player started...'
    except:
      traceback.print_exc(file=sys.stdout)
      raise

  def listen_on(self, event_id):
    pygame.mixer.music.set_endevent(event_id)

  def play(self, file, start=0):
    prettyprint(COLORS.WHITE, 'PyGameBroadcast playing: %s' % file.filepath)
    try:
      pygame.mixer.quit()
      pygame.mixer.init(file.bitrate)
      pygame.mixer.music.load(file.filepath)
      pygame.mixer.music.play(0, start)
      self.playing = True
    except pygame.error:
      prettyprint(COLORS.RED, 'Could not play %s! (%s)' % (file.filepath, pygame.get_error()))
      self.stop()
      raise

  def stop(self):
    try:
      pygame.mixer.music.stop()
    except pygame.error:
      prettyprint(COLORS.RED, 'Could not stop player! (%s)' % pygame.get_error())
      raise
    self.playing = False

  def set_volume(self, value):
    pygame.mixer.music.set_value(value)

  def get_volume(self, value):
    return pygame.mixer.music.get_value()

  def poll(self):
    return pygame.event.poll()

class OSXEventObject:
  def __init__(self):
    self.type = None

class OSXBroadcast():
  def __init__(self):
    self.play_event = OSXEventObject()
    self.timer = None
    self.event_id = None
    self.playing = False

  def play_end_handler(self):
    self.play_event.type = self.event_id

  def listen_on(self, event_id):
    self.event_id = event_id
    pass

  def clear(self):
    self.play_event.type = None
    if self.timer is not None:
      self.timer.cancel()
    self.playing = False

  def play(self, file, start=0):
    try:
      self.clear()
      prettyprint(COLORS.YELLOW, 'Playing file, %s' % file.filepath)
      call(['afplay', file.filepath])
      self.timer = Timer(file.length, self.play_end_handler)
      self.timer.start()
      self.playing = True
    except:
      self.stop()
      traceback.print_exc(file=sys.stdout)

  def stop(self):
    self.clear()
    call(['killall', 'afplay'])

  def set_volume(self, value):
    pass

  def get_volume(self, value):
    return 1.0

  def poll(self):
    return self.play_event