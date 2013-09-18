import os
import re
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TDRC
from mutagen.easyid3 import EasyID3

class AudioItem:

  source = None
  year_regex = re.compile('(\d{4})', re.IGNORECASE)

  def __init__(self, path):
    self.source = File(path, easy=True)

  def get_length(self):
    return self.source.info.length

  def has_defined_year(self):
    return self.get_year() is not None

  def get_year(self):
    value = None
    if 'date' in self.source.tags:
      value = self.source.tags["date"][0].encode('ascii','ignore')
      value = str(self.year_regex.match(value).group())
    return value