
class Dial:
  def __init__(self):
    self.listeners = []
    self.input_value = 0
    self.minimum_value = 0
    self.maximum_value = 100

  def add_listener(self, listener):
    self.listeners.append(listener)

  def notify_listeners(self):
    for listener in self.listeners:
      listener(self.input_value)

  def range(self, min_value, max_value):
    self.minimum_value = min_value
    self.maximum_value = max_value

  def set_value(self, percentage):
    print 'Dial.set_value() :: min: %d, max: %d' % (self.minimum_value, self.maximum_value)
    self.input_value = int(self.minimum_value + round((self.maximum_value - self.minimum_value) * percentage))
    self.notify_listeners()