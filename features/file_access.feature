Feature: Files from directory added to the list
  As an owner of Ra-dio
  I want to have audio files read from a target directory
  So that they are accessible by the program

  Scenario: MP3 File found in the root of target directory
    Given I have defined a target directory at "./features/fixtures/audio"
    And I have an MP3 file located in the root of the target directory
    When I request to parse audio files
    Then The file is listed in the model

  Scenario: Non-MP3 file in root of target directory not read
    Given I have defined a target directory at "./features/fixtures/audio"
    And I have a file that is not extension MP3 in the root of the target directory
    When I request to parse audio files
    Then The non-MP3 is not added to the model listing

  Scenario: MP3 file found in subdirectory of target directory
    Given I have defined a target directory at "./features/fixtures/audio"
    And I have an MP3 file within a subdirectory of the root of the target directory
    When I request to parse audio files
    Then The file in the subdirectory is listed in the model