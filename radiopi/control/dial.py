
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

  def set_roaming(self):
    self.input_value = self.minimum - 1
    self.notify_listeners()

  def set_value(self, percentage):
    new_value = int(self.minimum + round((self.maximum - self.minimum) * percentage))
    if self.input_value != new_value:
      self.input_value = new_value
      self.notify_listeners()