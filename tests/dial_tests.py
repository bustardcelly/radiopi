import mock

from nose.tools import *
from radiopi.control.dial import Dial

class Observer():
  def __init__(self):
    self.value = 0

  def handler(self, value):
    self.value = value

def test_set_range():
  dial = Dial()
  dial.range(35, 55)
  assert_equals(dial.minimum, 35, 'Expected %d, was %d' % (35, dial.minimum))

def test_value_in_range_with_base_zero():
  dial = Dial()
  observer = Observer()
  dial.add_listener(observer.handler)
  dial.range(0, 50)
  dial.set_value(0.5)
  product = observer.value
  assert_equals(product, 25, 'Expected %d, was %d' % (25, product))

def test_value_in_range_with_normal_year_range():
  dial = Dial()
  observer = Observer()
  dial.add_listener(observer.handler)
  dial.range(1997, 2013)
  dial.set_value(0.5)
  product = observer.value
  assert_equals(product, 2005, 'Expected %d, was %d' % (2005, product))

def test_value_round():
  dial = Dial()
  observer = Observer()
  dial.add_listener(observer.handler)
  dial.range(1997, 2000)
  dial.set_value(0.5)
  product = observer.value
  assert_equals(product, 1999, 'Expected %d, was %r' % (1999, product))

@mock.patch('radiopi.control.dial.Dial')
def test_listener_notification_on_set_value(control_Dial):
  control_Dial.notify.return_value = mock.Mock(['notify_listeners'])

  dial = control_Dial()
  observer = Observer()
  dial.add_listener(observer.handler)
  dial.range(0, 50)
  dial.set_value(0.5)
  control_Dial.assert_called_once()

def test_observer_notification_with_ranged_value():
  dial = Dial()
  observer = Observer()
  observer.handler = mock.Mock(['handler'])
  dial.add_listener(observer.handler)
  dial.range(1997, 2013)
  dial.set_value(0.5)
  observer.handler.assert_called_once_with(2005)