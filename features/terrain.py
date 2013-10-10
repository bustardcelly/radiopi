from lettuce import *

@after.each_feature
def print_audio_directory_files(feature):
  # print 'location: %s' % world.directory.location
  # print 'filepaths: %r' % world.directory.filepaths
  # if hasattr(world, 'radio'):
  #   print 'station queue index: %d' % world.radio.station.index
  pass