@echo off
setlocal enabledelayedexpansion

if "%~1" neq "" (
    set "VERSION=%~1"
) else (
    :prompt
    set "VERSION="
    set /p "VERSION=Enter version number: "
    
    if "!VERSION!"=="" (
        echo Enter a version number (ex: 0.0.0)
        goto prompt
    )
)

pyinstaller --onefile src/tracker.py

mkdir ".\releases\%VERSION%"
mkdir ".\releases\%VERSION%\settings"

echo %VERSION%

copy ".\dist\tracker.exe" ".\releases\%VERSION%\%VERSION%-tracker.exe"
robocopy "data/" "releases/%VERSION%/data/" /s /e
copy ".\settings\sample_settings.json" ".\releases\%VERSION%\settings\settings.json"

powershell Compress-Archive -Path "releases/%VERSION%/*" -DestinationPath "releases/%VERSION%/%VERSION%.zip" -Force