import os
import logging
from lettuce import *
from radiopi.file.audiodir import AudioDirectory

logger = logging.getLogger(__name__)

def resolve_directory(root, filename):
  return os.path.abspath(os.path.join(root, filename));

# @Given
@step('I have defined a target directory at "([^"]*)"')
def have_target_directory_defined(step, location):
  world.location = location
  world.directory = AudioDirectory(location)

# @Given
@step('I have an MP3 file located in the root of the target directory')
def have_file_in_root_target_directory(step):
  # set in /fixtures
  pass

# @Given
@step('I have a file that is not extension MP3 in the root of the target directory')
def have_non_valid_file_in_root_target_directory(step):
  # set in /fixtures
  pass

# @Given
@step('I have an MP3 file within a subdirectory of the root of the target directory')
def have_file_in_subdirectory_of_target_directory(step):
  # set in /fixtures
  pass

# @When
@step('I request to parse audio files')
def when_parse_audio_files(step):
  world.directory.parse();

# @Then
@step('The file is listed in the model')
def then_file_is_listed_on_model(step):
  filepath = resolve_directory(world.location, '09 - Anything Can Happen.mp3')
  assert filepath in world.directory.filepaths, ('Should contain %s file.' % filepath)

# @Then
@step('The non-MP3 is not added to the model listing')
def then_non_audio_file_is_not_listed_on_model(step):
  filepath = resolve_directory(world.location, 'somefile.txt')
  assert filepath not in world.directory.filepaths, ('Should not contain %s file.' % filepath)

# @Then
@step('The file in the subdirectory is listed in the model')
def then_file_in_subdir_is_on_model(step):
  filepath = resolve_directory('%s/%s' % (world.location, 'subdir'), 'b - love rap.mp3')
  assert filepath in world.directory.filepaths, ('Should contain %s from /subdir subdirectory.' % filepath)

