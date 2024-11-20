import pysondb as db
import os
import json


class LocalOutput():
    def __init__(self, cwd):
        json_db = self.initialize_db(cwd)
        
    # Creates a new json DB by copying the skeleton and overwriting previous DB
    def initialize_db(self, cwd):
        with open(os.join(cwd, "data", "skeleton.json"), "r") as f:
            skeleton_data = json.load(f)
        with open(os.join(cwd, "data", "data.json"), "w") as f:
            json.dump(skeleton_data, f)
        return db.getDb(os.join(cwd, "data", "data.json"))

    def update_db(self, adv_data):
        for adv, info in adv_data.items():
            current_data = self.json_db.getById(adv)
            current_data["progress"] = info[0]
            current_data["completed"] = info[3]
            current_data["incomplete"] = info[2]
            self.json_db.updateById(adv, current_data)