from random import shuffle

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
    file = self.queue[0]
    start = range_util.random(4, file.length * 0.25)
    play(file, start)

  def stop(self):
    pass

  def play(self, file, start=0):
    pass

class StaticStation(Station):
  def __init__(self, queue=None):
    self.queue = [AudioItem('path/to/static.mp3')]
