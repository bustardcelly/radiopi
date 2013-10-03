import os
from nose.tools import *
from radiopi.os.audiodir import AudioDirectory
from radiopi.model.session import Session

session = None
directory = AudioDirectory(os.path.join('.', 'features/fixtures/audio'))

def setup_session():
  global session
  session = Session()
  session.inflate(directory.parse())

def teardown_session():
  global session
  session = None

@with_setup(setup_session, teardown_session)
def test_session_start_year():
  expected_start = 1997
  assert_equals(session.start_year(), expected_start, 'Expected start year to be %d, was %d' % (expected_start, session.start_year()))

@with_setup(setup_session, teardown_session)
def test_session_end_year():
  expected_end = 2013
  assert_equals(session.end_year(), expected_end, 'Expected start year to be %d, was %d' % (expected_end, session.end_year()))

@with_setup(setup_session, teardown_session)
def test_get_items_by_year():
  itemslength = len(session.get_items(2013))
  assert_equals(itemslength, 1, 'Expected listing of 1 items from 2013, was %d' % itemslength );

@with_setup(setup_session, teardown_session)
def test_get_items_empty_from_year():
  itemslength = len(session.get_items(1984))
  assert_equals(itemslength, 0, 'Expected listing of 0 items from 1997, was %d' % itemslength );
