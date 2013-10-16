from lettuce import *
from radiopi.model.session import Session
from radiopi.file.audiodir import AudioDirectory

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
@step('The amount of files in the station map of the session is the same as from the list on audio dir')
def then_amount_of_files_exact_in_map(steps):
  count = 0
  for key in world.session.stations:
    count = count + world.session.stations[key].length()

  filepath_len = len(world.directory.filepaths)
  assert count == filepath_len, 'File length was %d, should be %d.' % (count, filepath_len)

# @Then
@step('The files without a year tag in ID3 are uncategorized')
def then_the_files_without_a_year_are_uncategorized(steps):
  uncategorized_length = len(world.session.stations[Session.UNCATEGORIZED_KEY].queue)
  assert uncategorized_length == 2, 'File length without date value should be 2, was %d' % uncategorized_length

# @Then
@step('The files with a year tag in ID3 are listed by year key')
def then_files_with_year_are_categorized_by_year_key(steps):
  listing = world.session.stations['1997'].queue
  assert len(listing) == 1, 'File length for year 1997 should be 1, was %d' % len(listing)