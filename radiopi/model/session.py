from radiopi.model.audioitem import AudioItem
from radiopi.model.station import Station, StaticStation

class Session:

  UNCATEGORIZED_KEY = 'N/A'

  def __init__(self):
    self.stations = {}
    self.static = StaticStation()
    self.stations[Session.UNCATEGORIZED_KEY] = Station()
    self.year_listing = []

  def inflate(self, paths):
    for f in paths:
      audio = AudioItem(f)
      if not audio.year is None:
        year_tag = str(audio.year)
        if not year_tag in self.stations:
          self.stations[year_tag] = Station()
        self.stations[year_tag].add_item(audio)
      else:
        self.stations[Session.UNCATEGORIZED_KEY].add_item(audio)
    self.generate_listing_by_year()
    self.shuffle()

  def generate_listing_by_year(self):
    for key in self.stations:
      if not key == Session.UNCATEGORIZED_KEY:
        self.year_listing.append(int(key))
    sorted(self.year_listing, key=int)

  def start_year(self):
    return self.year_listing[0] if not len(self.year_listing) == 0 else -1

  def end_year(self):
    return self.year_listing[len(self.year_listing) - 1] if not len(self.year_listing) == 0 else -1

  def shuffle(self):
    for key, value in self.stations.iteritems():
      value.shuffle_items()

  def get_station(self, year):
    str_year = str(year)
    return self.static if not str_year in self.stations else self.stations[str_year]

  def print_listing(self):
    for key, value in self.stations.iteritems():
      print '%s:\n%s' % (key, value)

