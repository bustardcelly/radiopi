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

  def play(self, file, start=0):
    print 'PyGameBroadcast playing: %s' % file.filename
    try:
      pygame.mixer.music.load(file.filename)
      pygame.mixer.music.play(0, start)
      self.playing = True
    except pygame.error:
      print 'Could not play %s! (%s)' % (file.filename, pygame.get_error())
      self.stop()
      raise

  def stop(self):
    try:
      pygame.mixer.music.stop()
    except pygame.error:
      print 'Could not stop player! (%s)' % pygame.get_error()
      raise
    
    self.playing = False