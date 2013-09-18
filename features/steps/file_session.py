from lettuce import *
from radiopi.os.audiodir import AudioDirectory
from radiopi.model.session import Session

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

# @Then
@step('The files with a year tag in ID3 are listed by year key')
def then_files_with_year_are_categorized_by_year_key(steps):
  listing = world.session.files['1997']
  assert len(listing) == 1, 'File length for year 1997 should be 1, was %d' % len(listing)