import os
import json


class LocalOutput():
    def __init__(self, settings):
        cwd = settings['cwd']
        self.file_path = settings["path_to_advancements_json"]
        self.skeleton_path = os.path.join(cwd, "data", "skeleton.json")
        self.stats_file_path = settings["path_to_stats_json"]
        self.stats_skeleton_path = os.path.join(cwd, "data", "stats_skeleton.json")
        
    # Creates a new json DB by copying the skeleton and overwriting previous DB
    def load_data(self, file_path):
        with open(file_path, "r") as f:
            return json.load(f)
        
    def write_data(self, file_path, data):
        with open(file_path, "w") as f:
            return json.dump(data, f)
        
    def update_db(self, adv_data, stats_data):
        self.update_db_adv(adv_data)
        self.update_db_stats(stats_data)

    def update_db_adv(self, adv_data):
        data = self.load_data(self.skeleton_path)
        for key in data:
            if key in adv_data:
                info = adv_data[key]
                data[key]["progress"] = info[0]
                data[key]["completed"] = info[3]
                data[key]["incomplete"] = info[2]
        self.write_data(self.file_path, data)

    def update_db_stats(self, stats_data):
        data = self.load_data(self.stats_skeleton_path)
        for key in data:
            data[key]["progress"] = stats_data.get("value", 0)

        self.write_data(self.file_path, data)