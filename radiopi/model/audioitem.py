import os
import re
import json
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TDRC
from mutagen.easyid3 import EasyID3

def filepath_title(path):
  return os.path.basename(path)

class AudioItemObject:

  year_regex = re.compile('(\d{4})', re.IGNORECASE)
  metaprops = ['artist', 'album', 'filepath']
  UNAVAILABLE_FIELD = 'N/A'

  def __init__(self, obj):
      self.audio_object = obj

  def __getattr__(self, name):
    if name is 'filename':
      return self.filepath
    if name in AudioItemObject.metaprops:
      return self.audio_object[name].encode('utf-8')
    elif name is 'length':
      return self.audio_object['length']
    elif name is 'title':
      title = self.audio_object['title'].encode('utf-8')
      return title if title != AudioItemObject.UNAVAILABLE_FIELD else filepath_title(self.filepath)
    elif name is 'year':
      value = self.audio_object['year'].encode('utf-8')
      if value != AudioItemObject.UNAVAILABLE_FIELD:
        value = str(AudioItemObject.year_regex.match(value).group())
      else:
        print "[WARN] - %s has no year" % self.filepath
      return value
    elif name is 'bitrate':
      return self.audio_object['bitrate']
    elif name is 'image':
      return File(self.filepath).tags['APIC:'].data
    else:
      return object.__getattribute__(self, name)

  def __str__(self):
    return json.dumps({\
      'artist': self.artist, \
      'title': self.title, \
      'album': self.album, \
      'filepath': self.filepath, \
      'length': self.length, \
      'year': self.year, \
      'bitrate': self.bitrate\
      }, indent=2)

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
      return title if title != AudioItem.UNAVAILABLE_FIELD else filepath_title(self.filepath)
    elif name in AudioItem.metaprops:
      return self.value_from_tag(name)
    elif name is 'year':
      value = self.value_from_tag('date')
      if value != AudioItem.UNAVAILABLE_FIELD:
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
      'filepath': self.filepath, \
      'length': self.length, \
      'year': self.year\
      }, indent=2)