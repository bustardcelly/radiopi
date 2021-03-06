import os
from nose.tools import *
from radiopi.model.audioitem import AudioItem

filepath = os.path.abspath(os.path.join('.', 'features/fixtures/audio/09 - Anything Can Happen.mp3'))
audioitem = AudioItem(filepath)

def test_filepath_access():
  path = audioitem.filename
  assert_equals(path, filepath, 'Filepath exposed on audioitem should be %s, was %s' % (filepath, path))

def test_year_access():
  expected_year = '1997'
  assert_equals(audioitem.year, expected_year, 'Defined year in tag should be accessbile. Expected %s, was %s' % (expected_year, audioitem.year))

def test_year_access_type():
  assert isinstance(audioitem.year, str), 'Return type of year should be str'

def test_length_access_type():
  assert isinstance(audioitem.length, float), 'Return type of file length should be float (in seconds)'

# Just testing that something is returned. Doesn't matter if real value or 'N/A'
def test_artist_access_type():
  assert isinstance(audioitem.artist, str), 'Return type of artist should be str'
  assert_not_equal(audioitem.artist, AudioItem.UNAVAILABLE_FIELD, 'Artist should be returned properly is available from tag.')

def test_title_access_type():
  assert isinstance(audioitem.title, str), 'Return type of title should be str'
  assert_not_equal(audioitem.title, AudioItem.UNAVAILABLE_FIELD, 'Title should be returned properly is available from tag.')

def test_album_access_type():
  assert isinstance(audioitem.album, str), 'Return type of album should be str'
  assert_not_equal(audioitem.album, AudioItem.UNAVAILABLE_FIELD, 'Album should be returned properly is available from tag.')