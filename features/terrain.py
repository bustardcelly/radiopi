from lettuce import *

@after.each_feature
def print_audio_directory_files(feature):
  # print 'location: %s' % world.directory.location
  # print 'filepaths: %r' % world.directory.filepaths
  print 'session files: %r' % 0 if not hasattr(world, 'session') else world.session.files
  pass