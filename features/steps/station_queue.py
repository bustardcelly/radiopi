import sys
import mock

from mock import ANY
from lettuce import *
from nose.tools import *
from radiopi.model.station import MIN_START_TIME_MS
from radiopi.model.station import Station
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

  station = Station(listing)
  station.play = mock.Mock(wraps=station.play)
  
  session = Session()
  session.stations['2005'] = station

  radio = Radio(session)
  radio.change_station = mock.Mock(wraps=radio.change_station)

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

# @And
@step('The last item in the queue has been reached and finished')
def when_index_in_queue_is_at_end(steps):
  world.radio.station.next()
  world.radio.station.next()

# @Then
@step('The list of files associated with corresponding year are queued')
def then_file_list_is_queued(steps):
  world.radio.change_station.assert_called_with(world.session.get_station(2005))

# @Then
@step('The first file in the associated queue is requested to be played at a random start time')
def then_file_is_played_at_random_time(steps):
  station = world.session.get_station(2005)
  item = station.queue[0]
  start_time = world.radio.station.play.call_args[0][1]
  world.radio.station.play.assert_called_with(item, ANY)
  assert_is_instance(start_time, int)
  assert start_time >= MIN_START_TIME_MS and start_time <= item['length'], \
    'Expected start time to lie between %d and %d, was %d' % (MIN_START_TIME_MS, item['length'], start_time)

@step('The first item from the queue is requested to be played again at 0 start time')
def then_the_queue_is_started_over(steps):
  station = world.radio.station
  item = station.queue[0]
  station.next()
  station.play.assert_called_with(item, 0)
