import os, csv, json
import logging
from utils import retry_on_exception

logger = logging.getLogger(__name__)

class AdvMonitor:
    def __init__(self, adv_folder, cwd, required_advs):
        self.adv_folder = adv_folder
        self.cwd = cwd
        self.advancements_list = required_advs
        self.items_list = self.get_data("item_to_adv.csv")
        self.criteria = self.get_data("adv_criteria_requirements.json")


    def check_item_progress(self, curr_advancements):
        completed_items = []
        for item, adv_path in self.items_list:
            if adv_path not in curr_advancements:
                continue
            if item in curr_advancements[adv_path]["criteria"]:
                completed_items.append(item)
        return set(completed_items)
    

    def get_max_item_progress(self, curr_items):
        max_item_uuid = max(curr_items, key=lambda k: len(curr_items[k]))
        
        super_set = curr_items[max_item_uuid]
        item_to_uuid = {item: max_item_uuid for item in curr_items[max_item_uuid]}

        
        for uuid, item_set in curr_items.items():
            super_set = super_set.union(item_set)
            for item in item_set:
                if item not in item_to_uuid:
                    item_to_uuid[item] = uuid
        return (max_item_uuid, item_to_uuid)


    def check_adv_progress(self, curr_advancements):
        """
        Reads through advancements json to measure progress towards goal.
        """

        adv_progress = {}
        for adv_path in self.advancements_list:
            if adv_path not in curr_advancements:
                continue

            adv_criteria = self.criteria[adv_path]
            adv_player = curr_advancements[adv_path]

            num_criteria = len(adv_criteria)
            completed = 0
            incomplete = []
            is_complete = False

            if adv_player["done"] == True:
                # All criteria is already met
                is_complete = True
                completed = num_criteria
            else:
                player_progress = set(adv_player["criteria"].keys())
                # Arrays in arrays means criteria is defined by requirements
                # One item from each grouping needs to be completed
                # (AND logic across arrays, OR logic within arrays)
                # If there are no arrays, then it's AND logic with everything
                or_logic = type(adv_criteria[0]) == list

                if not or_logic:
                    # AND Logic. All Criteria must be completed.
                    adv_criteria = set(adv_criteria)
                    incomplete = list(adv_criteria.difference(player_progress))
                    completed = len(player_progress)
                else:
                    # OR Logic. All criteria groups need one thing completed.
                    for criteria_group in adv_criteria:
                        if any(
                            criterion in player_progress for criterion in criteria_group
                        ):
                            completed += 1
                        else:
                            incomplete.append(criteria_group)
            """
            Adv_progress format:
            [0] : % complete (float)
            [1] : Fraction representation of progress (str)
            [2] : Incomplete criteria, if applicable (str)
            [3] : Is adv complete (bool)
            """
            adv_progress[adv_path] = (
                round(completed / num_criteria, 5),
                f"'{completed}/{num_criteria}",
                self.incomplete_advs_to_string(incomplete),
                is_complete,
            )
        return adv_progress

    def incomplete_advs_to_string(self, incomplete):
        if len(incomplete) == 0:
            return ""
        if type(incomplete[0]) != list:
            return ", ".join(incomplete)
        incomplete_strs = []
        for group in incomplete:
            incomplete_strs.append(" or ".join(group))
        return ", ".join(incomplete_strs)

    def get_max_progression(self, player_progress):
        """
        Reads through a list of player progress from check_progress
        Builds a list of all the players and returns the players data with the most progress
        for each individual advancement
        Returns adv progress tuple with a uuid appended
        """
        max_progress = {}
        for adv_path in self.advancements_list:
            for uuid in player_progress:
                if adv_path not in player_progress[uuid]:
                    continue
                info = player_progress[uuid][adv_path]
                if adv_path not in max_progress or max_progress[adv_path][0] < info[0]:
                    # Connect player to the progress
                    if info[0] < 1:
                        info = info + (uuid,)
                    else:
                        info = info + (None,)
                    max_progress[adv_path] = info
                    
        return max_progress
    
    def check_adv_directory(self):
        """
        Reads through advancements directory and manages all the data.
        """
        player_adv_progress = {}
        player_item_progress = {}
        for filename in os.listdir(self.adv_folder):
            if not filename.endswith(".json"):
                continue
            data = self.read_adv_file(filename)
            uuid = filename[:-5]

            adv_progress = self.check_adv_progress(data)
            item_progress = self.check_item_progress(data)

            player_item_progress[uuid] = item_progress
            player_adv_progress[uuid] = adv_progress
        max_item_progress = self.get_max_item_progress(player_item_progress)
        max_adv_progress = self.get_max_progression(player_adv_progress)
        
        return (max_adv_progress, max_item_progress)

    def get_data(self, filename):
        data_list = []
        with open(
            os.path.join(self.cwd, "data", filename), mode="r", encoding="utf-8"
        ) as f:
            if filename.endswith(".json"):
                return json.load(f)
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                data_list.append(row)
        return data_list
    
    # Probably useless unless advancement folder is updated more frequently
    def get_AL_progress(self, progress, adv="blazeandcave:bacap/advancement_legend"):
        if adv in progress:
            return progress[adv][1]
        return f"0/{self.criteria[adv]}"
    
    @retry_on_exception(json.decoder.JSONDecodeError)
    def read_adv_file(self, filename):
        with open(os.path.join(self.adv_folder, filename)) as f:
            data = json.load(f)
        return data