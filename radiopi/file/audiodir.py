import os
import re
import json

extension = re.compile('^(?!._)(.*?).m(p3|4a)', re.IGNORECASE)

class AudioDirectory:

  location = None
  filepaths = None

  def __init__(self, location):
    self.location = location

  def parse(self):
    global extension
    self.filepaths = []
    for root, dirs, files in os.walk(self.location):
      for f in files:
        if extension.match(f):
          self.filepaths.append(os.path.abspath(os.path.join(root, f)))
    return self.filepaths

class AudioJSON:

    data = None
    filepaths = None

    def __init__(self, jsonFile):
        with open(jsonFile) as data_file:
            self.data = json.load(data_file)

    def parse(self):
        global extension
        self.filepaths = []
        if self.data is not None:
            for key, value in self.data.items():
                for itemKey, itemValue in value.items():
                    if itemKey == "files":
                        for item in itemValue:
                            self.filepaths.append(item["filename"].encode('utf-8'))
        return self.filepaths