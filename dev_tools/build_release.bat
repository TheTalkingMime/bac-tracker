@echo off
setlocal enabledelayedexpansion

set /p "VERSION=Enter version number (ex: 0.0.0): "

pyinstaller --onefile ../tracker/src/tracker.py

if not exist ".\releases\" (
    mkdir ".\releases\"
)

mkdir ".\releases\%VERSION%"
mkdir ".\releases\%VERSION%\settings"

echo %VERSION%

copy ".\dist\tracker.exe" ".\releases\%VERSION%\%VERSION%-tracker.exe"
robocopy "../tracker/data/" "releases/%VERSION%/data/" /s /e
copy "..\tracker\settings\sample_settings.json" ".\releases\%VERSION%\settings\settings.json"

powershell Compress-Archive -Path "releases/%VERSION%/*" -DestinationPath "releases/%VERSION%/%VERSION%.zip" -Force