import os
from lettuce import *
from radiopi.os.audiodir import AudioDirectory

class Session:

  files = None

  def __init__(self):
    self.files = {}

  def inflate(self, paths):
    for f in paths:
      self.files[f] = f

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
  filepath_len = len(world.directory.filepaths)
  filemap_len = len([key for key in world.session.files])
  assert filemap_len == filepath_len, 'File length was %d, should be %d.' % (filemap_len, filepath_len)
