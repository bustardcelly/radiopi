import os
from lettuce import *
from radiopi.os.audiodir import AudioDirectory
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TDRC
from mutagen.easyid3 import EasyID3

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

class AudioItem:

  source = None

  def __init__(self, path):
    self.source = File(path, easy=True)

  def get_length(self):
    return self.source.info.length

  def has_defined_year(self):
    return self.get_year() is not None

  def get_year(self):
    # TODO: Parse date into year.
    return self.source.tags["date"][0].encode('ascii','ignore') if 'date' in self.source.tags else None

# @Given
@step('I have parsed an audio directory at "([^"]*)"')
def have_parsed_files_in_audio_dir(steps, location):
  world.location = location
  world.directory = AudioDirectory(location)
  world.session = Session()

# @When
@step('I supply parse result listing to the session')
def when_parsed_dir_is_given_to_session(steps):
  world.session.inflate(world.directory.parse())

# @Then
@step('The amount of files in the file map of the session is the same as from the list on audio dir')
def then_amount_of_files_exact_in_map(steps):
  amount = []
  for key in world.session.files:
    amount.extend(world.session.files[key])

  filepath_len = len(world.directory.filepaths)
  filemap_len = len(amount)
  assert filemap_len == filepath_len, 'File length was %d, should be %d.' % (filemap_len, filepath_len)

# @Then
@step('The files without a year tag in ID3 are uncategorized')
def then_the_files_without_a_year_are_uncategorized(steps):
  uncategorized_length = len(world.session.files[Session.UNCATEGORIZED_KEY])
  assert uncategorized_length == 2, 'File length without date value should be 2, was %d' % uncategorized_length
