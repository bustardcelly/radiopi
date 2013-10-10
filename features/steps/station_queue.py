import sys
import mock

from lettuce import *
from nose.tools import *
from radiopi.model.session import Session
from radiopi.control.dial import Dial
from radiopi.player.radio import Radio

def create(year, title, artist, filename, length):
  return {
    'year': year,
    'title': title,
    'artist': artist,
    'filename': filename,
    'length': length
  }

# @Given
@step('A list of audio files have been parsed for the session')
@mock.patch('radiopi.player.radio.Radio')
def given_list_of_files_on_session(steps, player_Radio):
  listing = []
  listing.append(create(2005, 'Hello, World', 'Foo, bar', 'foo.mp3', 10023))
  listing.append(create(2005, 'Goodbye, World', 'Baz, quo', 'bar.mp3', 344453))
  listing.append(create(2005, 'All UR Base Belong', 'to, us', 'baz.mp3', 402))
  
  session = Session()
  session.stations['2005'] = listing

  radio = Radio(session)
  radio.change_station = mock.Mock(['change_station'])

  dial = Dial()
  dial.range(1997, 2013)
  dial.add_listener(radio.dial_change_delegate)

  world.session = session
  world.radio = radio
  world.dial = dial

# @When
@step('I change the location of the Dial control')
def when_dial_control_value_changed(steps):
  world.dial.set_value(0.5)

# @When
@step('I change the station')
def when_dial_control_value_changed(steps):
  world.dial.set_value(0.5)

# @Then
@step('The list of files associated with corresponding year are queued')
def then_file_list_is_queued(steps):
  world.radio.change_station.assert_called_with(world.session.get_station(2005))

# @Then
@step('The first file in the associated queue is requested to be played at a random start time')
def then_file_is_played_at_random_time(steps):
  pass