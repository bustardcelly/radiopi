from random import shuffle
from random import randrange

MIN_START_TIME_MS = 4

class Station():
  def __init__(self, queue=None):
    self.queue = [] if queue is None else queue

  def add_item(self, audio_file):
    self.queue.append(audio_file)

  def length(self):
    return len(self.queue)

  def shuffle_items(self):
    shuffle(self.queue)

  def start(self):
    item = self.queue[0]
    start = randrange(MIN_START_TIME_MS, int(item['length'] * 0.25), 1)
    self.play(item, start)

  def stop(self):
    pass

  def play(self, item, start=0):
    pass

class StaticStation(Station):
  def __init__(self, queue=None):
    self.queue = [AudioItem('path/to/static.mp3')]
