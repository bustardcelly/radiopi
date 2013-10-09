import os
import re
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TDRC
from mutagen.easyid3 import EasyID3

class AudioItem:

  year_regex = re.compile('(\d{4})', re.IGNORECASE)
  metaprops = ['artist', 'title', 'album']
  UNAVAILABLE_FIELD = 'N/A'

  def __init__(self, path):
    self.source = File(path, easy=True)
    self.metadata = self.source.tags

  def __getattr__(self, name):
    if name is 'filename':
      return self.metadata.filename.encode('ascii', 'ignore')
    elif name is 'length':
      return self.source.info.length
    elif name in AudioItem.metaprops:
      return self.value_from_tag(name)
    elif name is 'year':
      value = self.value_from_tag('date')
      if value is not AudioItem.UNAVAILABLE_FIELD:
        value = str(AudioItem.year_regex.match(value).group())
      return value
    else:
      return object.__getattribute__(self, name)

  def value_from_tag(self, property):
    return self.metadata[property][0].encode('ascii', 'ignore') if property in self.metadata else AudioItem.UNAVAILABLE_FIELD