# bac-tracker
A tracker for Blaze and Caves Minecraft advancement pack. The tracker manages and puts all advancements in a google spreadsheet.

# Installation Instructions
Download bac-tracker.zip from [latest release](https://github.com/TheTalkingMime/bac-tracker/releases).

1. Unzip `bac-tracker.zip` You should have a data folder, settings folder, and an exe
2. Get a credentials json by following the instructions [here](https://www.youtube.com/watch?v=KIAo3Lgsk_Q), you only need to watch until 1:40 in the video. The rest of the video is specific to reset-tracker.
3. Put that json into the settings folder
4. Rename that json to `credentials.json`
5. Make a copy of the [1.21 Template](https://docs.google.com/spreadsheets/d/1Gyp1atdQ7QLEWRHBQ2AQFaTcg38jzZFPvaCOE4OeJhI/edit?gid=37686975#gid=37686975)
6. Open `credentials.json`
7. Inside you will find a field called `"client_email"` copy the associated value, and share it with your spreadsheet.
8. Open `settings.json`
9. Copy the spreadsheet link and paste it in between the quotation marks for the `"spreadsheet-link"` field.
10. Navigate to your world file and copy the full file path. (Ex: `.../saves/bac-world/`)
11. Paste the file path into the `settings.json` value for `"path_to_world"`
    a. Warning: back slashes are funky in strings, either convert all the slashes to forward slashes, or turn back slashes into double back slashes:
        - Acceptable: `.../saves/bac-world/` or `...\\saves\\bac-world\\`
        - Unacceptable: `...\saves\bac-world\`
12. Run tracker.exe and hope it all works
13. If you encounter any errors send the latest.log to assist.
         