import pygame
import traceback

class PyGameBroadcast():
  def __init__(self):
    try:
      pygame.init()
      pygame.mixer.init()
      self.playing = False
      print 'Pygame Broadcast player started...'
    except:
      traceback.print_exc(file=sys.stdout)
      raise

  def listen_on(self, event_id):
    pygame.mixer.music.set_endevent(event_id)

  def play(self, filepath, start=0):
    try:
      pygame.mixer.music.load(filepath)
      pygame.mixer.music.play(0, start)
      self.playing = True
    except pygame.error:
      self.stop()
      print 'File %s not found! (%s)' % (filepath, pygame.get_error())

  def stop(self):
    pygame.mixer.music.stop()
    self.playing = False