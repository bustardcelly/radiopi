from radiopi import prettyprint
from radiopi import COLORS


class Radio():
  def __init__(self, session, player=None):
    self.broadcast = player
    self.session = session
    self.station = None

  def change_station(self, to_station):
    if self.station is to_station:
      prettyprint(COLORS.YELLOW, 'Already playing station...')
      return
    elif not self.station is None:
      self.station.stop()

    self.station = to_station
    self.station.start(self.broadcast)

  def dial_change_delegate(self, year):
    prettyprint(COLORS.BLUE, 'Changing year to %r' % year)
    if(self.session.within_range(year)):
      self.change_station(self.session.get_station(year))
    else:
      self.change_station(self.session.get_search_station())
