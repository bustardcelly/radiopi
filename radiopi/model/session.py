import re

from radiopi.model.audioitem import AudioItem
from radiopi.model.station import Station
from radiopi.model.station import StaticStation
from radiopi.model.station import SearchStation

from radiopi import prettyprint
from radiopi import COLORS

class Session:

  UNCATEGORIZED_KEY = 'N/A'
  RA_REGEX = re.compile('^(.*?(rakim)[^$]*)$', re.IGNORECASE)

  def __init__(self):
    self.stations = {}
    self.static = StaticStation()
    self.search = SearchStation()
    self.stations[Session.UNCATEGORIZED_KEY] = Station()
    self.year_listing = []

  def inflate(self, paths):
    raStation = Station()
    for f in paths:
      try:
        audio = AudioItem(f)
        # prettyprint(COLORS.WHITE, 'Audio file: %s' % audio.title)
        # print 'Audio item found: %s' % audio
        if not audio.year is None:
          year_tag = str(audio.year)
          if not year_tag in self.stations:
            self.stations[year_tag] = Station()
          self.stations[year_tag].add_item(audio)
        else:
          self.stations[Session.UNCATEGORIZED_KEY].add_item(audio)
        # Store Rakim in a special place.
        if not audio.artist is None and Session.RA_REGEX.match(audio.artist):
          raStation.add_item(audio)
      except:
        prettyprint(COLORS.RED, 'Could not convert to audio file for station: %s' % f)
    self.generate_listing_by_year()
    if raStation.length() > 0:
      self.appendStation(raStation)
    self.shuffle()
    prettyprint(COLORS.BLUE, 'Year range, %d - %d' % (self.start_year(), self.end_year()))

  def appendStation(self, station):
    ending = self.end_year() + 1
    self.year_listing.append(ending)
    self.stations[str(ending)] = station
    prettyprint(COLORS.BLUE, 'Ra-dio Channel: %d, %d' % (ending, self.stations[ending].length()))

  def generate_listing_by_year(self):
    for key in self.stations:
      if not key == Session.UNCATEGORIZED_KEY:
        self.year_listing.append(int(key))
    self.year_listing.sort()

  def start_year(self):
    return self.year_listing[0] if not len(self.year_listing) == 0 else -1

  def end_year(self):
    return self.year_listing[len(self.year_listing) - 1] if not len(self.year_listing) == 0 else -1

  def within_range(self, year):
    return year >= self.start_year() and year <= self.end_year()

  def shuffle(self):
    for key, value in self.stations.iteritems():
      value.shuffle_items()

  def get_station(self, year):
    str_year = str(year)
    return self.static if not str_year in self.stations else self.stations[str_year]

  def get_search_station(self):
    return self.search

  def print_listing(self):
    for key, value in self.stations.iteritems():
      prettyprint(COLORS.WHITE, '%s:\n%s' % (key, value))

  def print_uncategorized(self):
    prettyprint(COLORS.RED, '%s' % self.stations[Session.UNCATEGORIZED_KEY])
