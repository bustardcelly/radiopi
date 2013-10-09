from random import shuffle
from audioitem import AudioItem

class Session:

  UNCATEGORIZED_KEY = 'N/A'

  def __init__(self):
    self.files = {}
    self.files[Session.UNCATEGORIZED_KEY] = []
    self.year_listing = []

  def inflate(self, paths):
    for f in paths:
      audio = AudioItem(f)
      if not audio.year is None:
        year_tag = str(audio.year)
        if not year_tag in self.files:
          self.files[year_tag] = []
        self.files[year_tag].append(audio)
      else:
        self.files[Session.UNCATEGORIZED_KEY].append(audio)
    self.generate_listing_by_year()

  def generate_listing_by_year(self):
    for key in self.files:
      if not key == Session.UNCATEGORIZED_KEY:
        self.year_listing.append(int(key))
    sorted(self.year_listing, key=int)

  def start_year(self):
    return self.year_listing[0] if not len(self.year_listing) == 0 else -1

  def end_year(self):
    return self.year_listing[len(self.year_listing) - 1] if not len(self.year_listing) == 0 else -1

  def shuffle_items(self):
    for key, value in self.files.iteritems():
      if len(value) > 1:
        shuffle(value)

  def get_items(self, year):
    str_year = str(year)
    return [] if not str_year in self.files else self.files[str_year]