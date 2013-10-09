
class Dial:
  def __init__(self):
    self.minimum = 0
    self.maximum = 100
    self.listeners = []
    self.input_value = 0

  def add_listener(self, listener):
    self.listeners.append(listener)

  def notify_listeners(self):
    for listener in self.listeners:
      listener(self.input_value)

  def range(self, min_value, max_value):
    self.minimum = min_value
    self.maximum = max_value

  def set_value(self, percentage):
    self.input_value = self.minimum + round((self.maximum - self.minimum) * percentage)
    self.notify_listeners()