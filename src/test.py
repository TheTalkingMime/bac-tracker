from scoreboard import Scoreboard
from pathlib import Path
import os

cwd = Path(__file__).resolve().parent.parent

#scoreboard = Scoreboard("C:/MultiMC/instances/1.21Modded/.minecraft/saves/tracker", cwd)
scoreboard = Scoreboard("C:/Users/Owner/Downloads/SWS BAC JUNE 2024", cwd)
scoreboard.check()