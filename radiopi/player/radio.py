
class Radio():
  def __init__(self, session):
    self.session = session
    self.file_queue = None

  def queue(self, file_listing):
    self.file_queue = file_listing

  def station_change_delegate(self, year):
    self.queue(self.session.get_items(year))
