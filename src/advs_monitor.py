import os, csv, json
import logging

logging.basicConfig(level=logging.DEBUG)

class AdvMonitor:
    def __init__(self, adv_folder, cwd, required_advs):
        self.adv_folder = adv_folder
        self.cwd = cwd
        self.advancements_list = required_advs
        self.items_list = self.get_data("item_to_adv.csv")
        self.criteria = self.get_data("adv_criteria_requirements.json")

    def check_advancements(self, curr):
        """
        Reads through advancements json to identify which advancements are completed.
        """
        completed_advs = set()
        for adv_path in self.advancements_list:
            if adv_path not in curr:
                continue
            if curr[adv_path]["done"] == True:
                completed_advs.add(adv_path)
        return completed_advs

    def check_items(self, curr_advancements):
        """
        Reads through advancements json to identify which items are completed.
        """
        completed_items = set()
        for item, adv in self.items_list:
            if adv not in curr_advancements:
                continue
            if item in curr_advancements[adv]["criteria"]:
                completed_items.add(item)
        return completed_items

    def check_progress(self, curr_advancements):
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
        Builds a list of all the players and how much they have completed
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
        # print(max_progress)
        # with open(os.path.join(self.cwd, 'data', 'output.csv'), 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     for k, v in max_progress.items():
        #         writer.writerow((k,) + v)

        # for uuid in player_progress:
        #     with open(os.path.join(self.cwd, 'data', f'{uuid}.csv'), 'w', newline='') as f:
        #         writer = csv.writer(f)
        #         for k, v in player_progress[uuid].items():
        #             writer.writerow((k,) + v)

        return max_progress

    def check_adv_directory(self):
        """
        Reads through advancements directory and manages all the data.
        """
        # max_completed_advs = set()
        max_completed_items = set()
        player_progress = {}
        for filename in os.listdir(self.adv_folder):
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(self.adv_folder, filename)) as f:
                data = json.load(f)

            # completed_adv = self.check_advancements(data)
            adv_progress = self.check_progress(data)
            completed_items = self.check_items(data)

            player_progress[filename[:-5]] = adv_progress
            # max_completed_advs = max(max_completed_advs, completed_adv, key=len)
            max_completed_items = max(max_completed_items, completed_items, key=len)
        max_progression = self.get_max_progression(player_progress)
        return (max_progression, max_completed_items)

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
