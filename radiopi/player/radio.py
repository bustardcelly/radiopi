
class Radio():
  def __init__(self, session, player=None):
    self.broadcast = player
    self.session = session
    self.station = None

  def change_station(self, to_station):
    if not self.station is None:
      self.station.stop()

    self.station = to_station
    self.station.start(self.broadcast)

  def dial_change_delegate(self, year):
    self.change_station(self.session.get_station(year))
