import nbtlib
import csv
import os
from logging_config import LOGGING_CONFIG
import logging
from utils import retry_on_exception
from gzip import BadGzipFile

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

class Scoreboard:
    def __init__(self, world_dir, cwd):
        self.scoreboard_path = os.path.join(world_dir, "data", "scoreboard.dat")
        self.prev_time = None
        self.scoreboards = {}
        reader = csv.reader(open(os.path.join(cwd, "data", "scoreboards.csv"), 'r'))
        for row in reader:
            #print(row)
            scoreboard, mode = row
            self.scoreboards[scoreboard] = mode

    def check(self):
        scores = {}

        for scoreboard in self.scoreboards:
            scores[scoreboard] = {"value": 0}

        objectives_tag = self.read_dat()

        for objective in objectives_tag:
            if objective['Objective'] in self.scoreboards:
                if self.scoreboards[objective['Objective']] == "max" and scores[objective['Objective']]["value"] < objective['Score']:
                    scores[objective['Objective']]["value"] = int(objective['Score'])
                    scores[objective['Objective']]["player"] = str(objective['Name'])
                if self.scoreboards[objective['Objective']] == "sum":
                    scores[objective['Objective']]["value"] += int(objective['Score'])
            
            if objective['Objective'] == 'bac_current_time' and objective['Name'] == 'time':
                current_time = objective['Score']
        output = ""
        
        for score in scores:
            logger.debug(f"{score}: {scores[score]}")
        
        logger.info(f"Current time: {int(current_time)}, {current_time == self.prev_time}")
        if current_time == self.prev_time:
            output = "Warning: bac_current_time hasn't updated"
        self.prev_time = int(current_time)
        return output, scores

    @retry_on_exception((TypeError, KeyError, BadGzipFile), retries=3, delay=2)
    def read_dat(self):
        with nbtlib.load(self.scoreboard_path) as file:
            objectives_tag = file['data']['PlayerScores']
        return objectives_tag
    