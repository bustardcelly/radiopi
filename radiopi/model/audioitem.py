import os
import re
import json
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TDRC
from mutagen.easyid3 import EasyID3

def filename_title(path):
  return os.path.basename(path)

class AudioItem:

  year_regex = re.compile('(\d{4})', re.IGNORECASE)
  metaprops = ['artist', 'album']
  UNAVAILABLE_FIELD = 'N/A'

  def __init__(self, path):
    self.filepath = path
    self.source = File(path, easy=True)
    self.metadata = self.source.tags
    self.image_data = None
    try:
      self.image_data = File(path).tags['APIC:'].data
    except:
      pass
#      print "No image found for file %s" % path

  def __getattr__(self, name):
    if name is 'filename':
      return self.filepath
    elif name is 'length':
      return self.source.info.length
    elif name is 'title':
      title = self.value_from_tag('title')
      return title if title is not AudioItem.UNAVAILABLE_FIELD else filename_title(self.filepath)
    elif name in AudioItem.metaprops:
      return self.value_from_tag(name)
    elif name is 'year':
      value = self.value_from_tag('date')
      if value is not AudioItem.UNAVAILABLE_FIELD:
        value = str(AudioItem.year_regex.match(value).group())
      return value
    elif name is 'image':
      return self.image_data
    else:
      return object.__getattribute__(self, name)

  def value_from_tag(self, property):
    return self.metadata[property][0].encode('ascii', 'ignore') if property in self.metadata else AudioItem.UNAVAILABLE_FIELD

  def __str__(self):
    return json.dumps({\
      'artist': self.artist, \
      'title': self.title, \
      'album': self.album, \
      'filename': self.filename, \
      'length': self.length, \
      'year': self.year\
      }, indent=2)