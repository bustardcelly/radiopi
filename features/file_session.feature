Feature: Files from audio directory parsed in to mapped listing by year
  In order to create a mapping of files by year we will map the listing from target audio directory

  Scenario: Files from audio directory listing available in map
    Given I have parsed an audio directory at "./features/fixtures/audio"
    When I supply parse result listing to the session
    Then The amount of files in the file map of the session is the same as from the list on audio dir

  Scenario: Files without year in ID3 tag added to uncategorized listing
    Given I have parsed an audio directory at "./features/fixtures/audio"
    When I supply parse result listing to the session
    Then The files without a year tag in ID3 are uncategorized

  Scenario: Files with year in ID3 tag added to listing with year as key
    Given I have parsed an audio directory at "./features/fixtures/audio"
    When I supply parse result listing to the session
    Then The files with a year tag in ID3 are listed by year key