## Paths
1. `bac_tracker` Should be stored adjacent to your world folder.
2. Will need to add the `bac_datapack` if trying to mess with parsing scripts.
   1. Just an unzipped version of the datapack
   


## Features Needed
 - [x] Overlay
   - [x] Browser source
 - [ ] Add more error catching
 - [ ] Create logs directory if doesn't exist
 - [ ] Add log handling so we don't get too many log files
 - [x] Progress column
   - [x] Displays total objectives completed for the advancement
   - [x] Maybe some clever way to display incomplete objectives without clogging the sheet
 - [x] Add log reading for faster updates
   - [x] track the completer
   - [x] track timestamp
   - [x] Add spreadsheet support
 - [x] Make main loop independent of code execution speed (reference system clock)
 - [x] Update references to 1.21 BAC pack
 - [ ] Implement settings
   - [ ] Make most things toggleable
 - [x] Make a local version of the overlay
   - [x] Maybe just localhost I guess
 - [ ] Make features of overlay configurable in settings
 - [ ] Optimize API calls (Can we update multiple sheets in one batch update?)
 - [ ] Merge changes with tj's statistics branch
 - [ ] Add a setup on script startup
   - [ ] Populate path
     - [ ] Auto-detect?
   - [ ] UI/NoUI options
 - [ ] 

## Future Features

 - [ ] Make a generalized parsing script for building the needed csvs
   - [ ] Implement this into the main script
   - [ ] Fix parsing for 65 hours of walking
 - [x] Push player heads to spreadsheet instead of player names
   - [x] Add UUID mappings to player names and vice versa
 - [ ] Overlay additions
     - [ ] Summary statistics
     - [ ] Maybe some scrolling statistics

## Bugs
 - [x] Random crashes that appeared in HBG run
   - [x] Unknown why
 - [x] Incorrect values being pushed for All Items/Blocks
   - [x] Happening because the sheet doesn't reset progress when it switches players
 - [x] Not pushing final update at end of HBG run


## Misc
 - [ ] Installation tutorial
 - [ ] Instructions for setting up tracker with any advancement pack
 - [ ] Modify datapack to remove 365 days requirement
 - [ ] Create executable and releases