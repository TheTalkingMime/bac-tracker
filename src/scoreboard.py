import nbtlib
import csv
import os

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

        with nbtlib.load(self.scoreboard_path) as file:
            objectives_tag = file['data']['PlayerScores']

            for objective in objectives_tag:
                if objective['Objective'] in self.scoreboards:
                    if self.scoreboards[objective['Objective']] == "max" and scores[objective['Objective']]["value"] < objective['Score']:
                        scores[objective['Objective']]["value"] = int(objective['Score'])
                        scores[objective['Objective']]["player"] = str(objective['Name'])
                    if self.scoreboards[objective['Objective']] == "sum":
                        scores[objective['Objective']]["value"] += int(objective['Score'])
                
                if objective['Objective'] == 'bac_current_time' and objective['Name'] == 'time':
                    current_time = objective['Score']
        
        for score in scores:
            print(f"{score}: {scores[score]}")
        
        output = "None"
        print(f"Current time: {int(current_time)}, {current_time == self.prev_time}")
        if current_time == self.prev_time:
            output = "Warning: bac_current_time hasn't updated"
        self.prev_time = int(current_time)
        return output, scores
