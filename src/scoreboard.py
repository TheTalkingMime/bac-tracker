import nbtlib
import os


class Scoreboard:
    def __init__(self, world_dir):
        self.scoreboard_path = os.path.join(world_dir, "data", "scoreboard.dat")
        self.prev_time = None
    def check(self):
        with nbtlib.load(self.scoreboard_path) as file:
            objectives_tag = file['data']['PlayerScores']

            for objective in objectives_tag:
                if objective['Objective'] == 'bac_current_time' and objective['Name'] == 'time':
                    current_time = objective['Score']
        output = "None"
        print(f"Current time: {int(current_time)}, {current_time == self.prev_time}")
        if current_time == self.prev_time:
            output = "Warning: bac_current_time hasn't updated"
        self.prev_time = int(current_time)
        return output
