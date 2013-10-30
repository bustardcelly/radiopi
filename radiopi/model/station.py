from random import shuffle
from random import randrange
from radiopi.model.audioitem import AudioItem

import radiopi.settings as settings

from radiopi import prettyprint
from radiopi import COLORS

MIN_START_TIME_MS = 4

class Station():
  def __init__(self, queue=None):
    self.player = None
    self.queue = [] if queue is None else queue

  def add_item(self, audio_file):
    self.queue.append(audio_file)

  def length(self):
    return len(self.queue)

  def shuffle_items(self):
    shuffle(self.queue)

  def start(self, player):
    item = self.queue[0]
    start_range = MIN_START_TIME_MS
    stop_range = round(item.length * 0.25)
    start_range = stop_range if stop_range < start_range else start_range
    stop_range = MIN_START_TIME_MS if start_range != MIN_START_TIME_MS else stop_range
    prettyprint(COLORS.WHITE, 'Starting station with: %s.' % item)
    start = randrange(start_range, stop_range, 1)
    self.player = player
    self.play(item, start)

  def stop(self):
    if not self.player is None:
      self.player.stop()

  def play(self, item, start=0):
    if not self.player is None:
      self.queue.remove(item)
      self.player.play(item, start)
      self.queue.append(item)

  def next(self):
    self.play(self.queue[0], 0)

  def current(self):
    item = self.queue[-1]
    return '%s%s%s' % (item.artist, settings.FILEDATA_DELIMITER, item.title)

  def __str__(self):
    return '\n'.join(str(item) for item in self.queue)

class SearchStation(Station):
  def __init__(self, queue=None):
    use_queue = queue
    if use_queue is None:
      use_queue = []
      for filepath in settings.SEARCH_FILES:
        use_queue.append(AudioItem(filepath))
    Station.__init__(self, use_queue)

  def current(self):
    return 'searching...'

class StaticStation(Station):
  def __init__(self, queue=None):
    Station.__init__(self, queue if queue is not None else [AudioItem(settings.STATIC_FILE)])

  def current(self):
    return '... dead air ...'
