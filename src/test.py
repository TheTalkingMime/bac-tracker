from scoreboard import Scoreboard
from stats import Statistics
from pathlib import Path
import os

cwd = Path(__file__).resolve().parent.parent

saves_path = "C:/MultiMC/instances/1.21Modded/.minecraft/saves/tracker"
#saves_path = "C:/Users/Owner/Downloads/SWS BAC JUNE 2024"

scoreboard = Scoreboard(saves_path, cwd)
scoreboard.check()

stats = Statistics(saves_path, cwd)
stats.check()