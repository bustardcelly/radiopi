import os
import re
import logging

class AudioDirectory:

  location = None
  filepaths = None
  extension = re.compile('(.*?).m(p3|4a)', re.IGNORECASE)

  def __init__(self, location):
    self.location = location

  def parse(self):
    self.filepaths = []
    for root, dirs, files in os.walk(self.location):
      for f in files:
        if self.extension.match(f):
          self.filepaths.append(os.path.abspath(os.path.join(root, f)))
    return self.filepaths