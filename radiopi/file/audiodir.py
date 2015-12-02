import sys
import os
import re
import json
from radiopi.model.audioitem import AudioItem
from radiopi.model.audioitem import AudioItemObject

from radiopi import prettyprint
from radiopi import COLORS

extension = re.compile('^(?!._)(.*?).m(p3|4a)', re.IGNORECASE)

class AudioDirectory:

  """
  Takes list of filepaths and converts them to Audio items
  """

  location = None
  files = None

  def __init__(self, location):
    self.location = location

  def parse(self):
    global extension
    self.files = []
    for root, dirs, files in os.walk(self.location):
      for f in files:
        if extension.match(f):
          filepath = os.path.abspath(os.path.join(root, f))
          try:
              self.files.append(AudioItem(filepath))
          except:
            e = sys.exc_info()[0]
            prettyprint(COLORS.RED, 'Could not convert to audio file for station: %s' % f)
            prettyprint(COLORS.RED, e)
    return self.files

class AudioJSON:

    """
    Takes JSON input generated from dirseal
    """

    data = None
    files = None

    def __init__(self, jsonFile):
        with open(jsonFile) as data_file:
            self.data = json.load(data_file)

    def parse(self):
        self.files = []
        if self.data is not None:
            for key, value in self.data.items():
                for itemKey, itemValue in value.items():
                    if itemKey == "files":
                        for item in itemValue:
                            self.files.append(AudioItemObject(item))
        return self.files