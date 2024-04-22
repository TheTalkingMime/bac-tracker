## Paths
1. `bac_tracker` Should be stored adjacent to your world folder.
2. Will need to add the `bac_datapack` if trying to mess with parsing scripts.
   1. Just an unzipped version of the datapack
   


## Features Needed
 - [ ] Overlay
   - [ ] Browser source
   - [ ] Summary statistics
     - [ ] Maybe some scrolling statistics
 - [ ] Add more error catching
 - [ ] Add log handling so we don't get too many logs
 - [x] Progress column
   - [x] Displays total objectives completed for the advancement
   - [x] Maybe some clever way to display incomplete objectives without clogging the sheet
 - [x] Add log reading for faster updates
   - [x] track the completer
   - [x] track timestamp
   - [x] Add spreadsheet support
 - [ ] Make API calls asynchronous

## Future Features
 - [ ] Add a setup on script startup
   - [ ] Populate path
   - [ ] UI/NoUI options
 - [ ] Make a generalized parsing script for building the needed csvs
   - [ ] Fix parsing for 65 hours of walking
 - [x] Push player heads to spreadsheet instead of player names
   - [x] Add UUID mappings to player names and vice versa


## Bugs
 - [ ] Random crashes that appeared in HBG run
   - [ ] Unknown why
 - [x] Incorrect values being pushed for All Items/Blocks
   - [x] Happening because the sheet doesn't reset progress when it switches players
 - [ ] Not pushing final update at end of HBG run


## Misc
 - [ ] Installation tutorial
 - [ ] Instructions for setting up tracker with any advancement pack
 - [ ] Modify datapack to remove 365 days requirement
 - [ ] Create an executable