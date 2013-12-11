Feature: File listing stored upon session inflate
  In order not to parse the same directory that was previously traversed we will hold a record of audio files.

  @skip
  Scenario: Parsed files are saved to disk as JSON based on year
    Given There is no record of previously parsing a directory
    And I have requested to parse a directory
    When The session is inflated
    Then The file results are serialized in JSON to disk

  @skip
  Scenario: Previous record does not match modification date of directory
    Given There is a previous record of parsing a directory
    When The modification date of the directory is later than the record file
    Then The modified files are added to the record
    And The record is saved back down to disk