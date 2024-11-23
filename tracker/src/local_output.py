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
        mapping = {
            "custom.aviate_one_cm": 100000000,
            "custom.walk_one_cm": 25000000,
            "custom.sprint_one_cm": 25000000,
            "custom.jump": 100000,
            "custom.crouch_one_cm": 1000000,
            "custom.swim_one_cm": 5000000,
            "custom.minecart_one_cm": 5000000,
            "custom.pig_one_cm": 1000000,
            "custom.horse_one_cm": 5000000,
            "custom.boat_one_cm": 5000000,
            "custom.strider_one_cm": 1000000,
            "custom.mob_kills": 25000,
            "custom.animals_bred": 2500,
            "custom.enchant_item": 250,
            "custom.traded_with_villager": 2500,
            "bac_day_count": 365,
            "bac_stat_food": 5000,
            "bac_stat_loot_chest": 500
        }

        for key in stats_data:
            data[key] = {
                "id": key,
                "progress": 0,
                "maxProgress": mapping.get(key, -1)
            }
            

        # for key in data:
        #     data[key]["progress"] = stats_data[key].get("value", 0)

        self.write_data(self.stats_file_path, data)