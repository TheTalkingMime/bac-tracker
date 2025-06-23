import nbtlib
import csv
import os
import logging
from utils import retry_on_exception
from gzip import BadGzipFile

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

        mapping = {}
        advancements = {}

        for objective in objectives_tag:
            objective = dict(objective)
            if objective['Objective'] in self.scoreboards:
                if self.scoreboards[objective['Objective']] == "max" and scores[objective['Objective']]["value"] < objective['Score']:
                    scores[objective['Objective']]["value"] = int(objective['Score'])
                    scores[objective['Objective']]["player"] = str(objective['Name'])
                if self.scoreboards[objective['Objective']] == "sum":
                    scores[objective['Objective']]["value"] += int(objective['Score'])
            
            if objective['Objective'] == 'bac_current_time' and objective['Name'] == 'time':
                current_time = objective.get('Score', 0)

            if objective['Objective'] == 'tracker_players':
                if str(objective['Name']) == '.total' or 'Score' not in objective:
                    continue
                mapping[int(objective['Score'])] = str(objective['Name'])
            if objective['Objective'] == 'tracker_advancement':
                advancements[str(objective['Name'])] = objective.get('Score', 0)
        
        # IBowSpam is a player with a question mark as their head, so it will look good on the spreadsheet
        mapped_advancements = {key: mapping.get(value, "IBowSpam") for key,value in advancements.items()}

        output = ""
        
        for score in scores:
            logger.debug(f"{score}: {scores[score]}")
        
        logger.info(f"Current time: {int(current_time)}, {current_time == self.prev_time}")
        if current_time == self.prev_time:
            output = "Warning: bac_current_time hasn't updated"
        self.prev_time = int(current_time)

        # Output is warning text
        # Scores is stats info
        return output, scores, mapped_advancements

    @retry_on_exception((TypeError, KeyError, BadGzipFile, EOFError), retries=3, delay=2)
    def read_dat(self):
        with nbtlib.load(self.scoreboard_path) as file:
            objectives_tag = file['data']['PlayerScores']
        return objectives_tag
    