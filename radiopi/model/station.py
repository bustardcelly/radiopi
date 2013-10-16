from random import shuffle
from random import randrange
from radiopi.settings import STATIC_FILE
from radiopi.model.audioitem import AudioItem

MIN_START_TIME_MS = 4

class Station():
  def __init__(self, queue=None):
    self.index = 0
    self.player = None
    self.queue = [] if queue is None else queue

  def add_item(self, audio_file):
    self.queue.append(audio_file)

  def length(self):
    return len(self.queue)

  def shuffle_items(self):
    shuffle(self.queue)

  def start(self, player):
    self.index = 0
    item = self.queue[self.index]
    start = randrange(MIN_START_TIME_MS, int(item['length'] * 0.25), 1)
    self.player = player
    self.play(item, start)

  def stop(self):
    if not self.player is None:
      self.player.stop()

  def play(self, item, start=0):
    if not self.player is None:
      self.player.start(item, start)

  def next(self):
    self.index = 0 if self.index == self.length() - 1 else self.index + 1
    self.play(self.queue[self.index], 0)

  def __str__(self):
    return '\n'.join(str(item) for item in self.queue)

class StaticStation(Station):
  def __init__(self, queue=None):
    default = [AudioItem(STATIC_FILE)]
    Station.__init__(self, default if queue is None else queue)
