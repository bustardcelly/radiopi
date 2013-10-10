import os
from nose.tools import *
from radiopi.os.audiodir import AudioDirectory
from radiopi.model.session import Session
from radiopi.model.station import Station

session = None
item_listing = []
directory = AudioDirectory(os.path.join('.', 'features/fixtures/audio'))

def create(year, title, artist):
  return {
    'year': year,
    'title': title,
    'artist': artist
  }

def setup_session():
  global session
  session = Session()
  session.inflate(directory.parse())

def setup_filled_session():
  global session
  global item_listing
  session = Session()
  item_listing.append(create(2001, 'Hello, World', 'Foo, bar'))
  item_listing.append(create(2001, 'Goodbye, World', 'Baz, quo'))
  item_listing.append(create(2001, 'All UR Base Belong', 'to, us'))
  session.stations['2001'] = Station(item_listing)

def teardown_session():
  global session
  session = None
  item_listing = []

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
  itemslength = session.get_station(2013).length()
  assert_equals(itemslength, 1, 'Expected listing of 1 items from 2013, was %d' % itemslength );

@with_setup(setup_session, teardown_session)
def test_get_items_empty_from_year():
  station = session.get_station(1984)
  assert_equals(station, None, 'Expected no station from 1984, was %r' % station );

@with_setup(setup_filled_session, teardown_session)
def test_shuffle_year_items():
  previous_list = item_listing[:]
  session.shuffle()
  assert_not_equal(previous_list, item_listing, 'Expected %r to be in different order than %r' % (previous_list, item_listing))