Feature: User changes to from station to station
  As an interactive user to Ra-dio
  I want to be notified when I have changes the station to a non-listed year-based station

  @skip
  Scenerio: Select of non-listed station queues static
    Given I have a session of year-based stations
    When I change the station to a year not listed
    Then I should be queued with a static file