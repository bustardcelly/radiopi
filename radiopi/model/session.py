from audioitem import AudioItem

class Session:

  files = None
  UNCATEGORIZED_KEY = 'N/A'

  def __init__(self):
    self.files = {}
    self.files[Session.UNCATEGORIZED_KEY] = []

  def inflate(self, paths):
    for f in paths:
      audio = AudioItem(f)
      if audio.has_defined_year():
        year_tag = audio.get_year()
        if not year_tag in self.files:
          self.files[year_tag] = []
        self.files[year_tag].append(audio)
      else:
        self.files[Session.UNCATEGORIZED_KEY].append(audio)