import pygame

class PyGameBroadcast():
  def __init__(self):
    pygame.init()
    pygame.mixer.init()
    self.playing = False

  def listen_on(self, event_id):
    pygame.mixer.music.set_endevent(event_id)

  def play(self, filepath, start=0):
    try:
      pygame.mixer.music.load(filepath)
    except pygame.error:
      print 'File %s not found! (%s)' % (filepath, pygame.get_error())
    pygame.mixer.music.play(0, start)

  def stop():
    pygame.mixer.music.stop()