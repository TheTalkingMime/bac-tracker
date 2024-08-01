import nbtlib
import csv
import json
import os

class Statistics:
    def __init__(self, world_dir, cwd):
        self.statistics_path = os.path.join(world_dir, "stats")
        self.statistics = {}
        reader = csv.reader(open(os.path.join(cwd, "data", "stats.csv"), 'r'))
        for row in reader:
            #print(row)
            statistic, mode = row
            self.statistics[statistic] = mode
            #split = statistic.split(".")
            #print(f"minecraft:{split[0]} minecraft:{split[1]}")

    def check(self):
        stats = {}

        for statistic in self.statistics:
            stats[statistic] = {"value": 0}

        stats_files = os.listdir(self.statistics_path)

        for file in stats_files:
            uuid = file[:-5]
            with open(os.path.join(self.statistics_path, file)) as f:
                current_file = json.load(f)

                for statistic in self.statistics:
                    split = statistic.split(".")
                    s = ["stats", f"minecraft:{split[0]}", f"minecraft:{split[1]}"]
                    if s[0] in current_file and s[1] in current_file[s[0]] and s[2] in current_file[s[0]][s[1]]:
                        if self.statistics[statistic] == "max" and current_file[s[0]][s[1]][s[2]] > stats[statistic]["value"]:
                            stats[statistic]["value"] = current_file[s[0]][s[1]][s[2]]
                            stats[statistic]["player"] = uuid
                        if self.statistics[statistic] == "sum":
                            stats[statistic]["value"] += current_file[s[0]][s[1]][s[2]]

        for stat in stats:
                print(f"{stat}: {stats[stat]}")
        return stats