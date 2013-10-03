import os
import re
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TDRC
from mutagen.easyid3 import EasyID3

class AudioItem:

  year_regex = re.compile('(\d{4})', re.IGNORECASE)
  UNAVAILABLE_FIELD = 'N/A'

  def __init__(self, path):
    self.source = File(path, easy=True)
    self.metadata = self.source.tags

  def get_filepath(self):
    return self.metadata.filename.encode('ascii', 'ignore')

  def get_length(self):
    return self.source.info.length

  def get_artist(self):
    return self.value_from_tag('artist')

  def get_title(self):
    return self.value_from_tag('title')

  def get_album(self):
    return self.value_from_tag('album')

  def has_defined_year(self):
    return self.get_year() is not None

  def get_year(self):
    value = None
    if 'date' in self.metadata:
      value = self.metadata["date"][0].encode('ascii', 'ignore')
      value = str(AudioItem.year_regex.match(value).group())
    return value

  def value_from_tag(self, property):
    return self.metadata[property][0].encode('ascii', 'ignore') if property in self.metadata else AudioItem.UNAVAILABLE_FIELD