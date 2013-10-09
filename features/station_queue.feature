Feature: Change to Dial value switches station and file queue
  As an interactive user to Ra-dio
  I want to listen to a different station (queue of files by year) when I change the location of the dial control

  Scenario: Files accessed by year based on Dial value
    Given A list of audio files have been parsed for the session
    When I change the location of the Dial control
    Then The list of files associated with corresponding year are queued

  @skip
  Scenario: First file is request to be played at random time
    Given A list of audio files have been parsed for the session
    When I change the station
    Then The first file in the associated queue is requested to be played at a random start time

  @skip
  Scenario: Queued file list is wrapped upon play
    Given A list of audio files have been parsed for the session
    When I change the station
    And The queue has started
    And The last item in the queue has been reached and finished
    Then The first item from the queue is requested to be played again at 0 start time