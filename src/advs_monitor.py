import os, csv, json

class AdvMonitor:
    def __init__(self, adv_folder, cwd):
        self.adv_folder = adv_folder
        self.cwd = cwd
        self.advancements_list = self.get_data(filename='advname_to_path.csv')
        self.items_list = self.get_data(filename='item_to_adv.csv')

    def check_advancements(self, curr):
        """
        Reads through an advancements json to identify which advancements are completed.
        """
        completed_advs = set()
        for _, adv in self.advancements_list:
            if adv not in curr:
                continue
            if curr[adv]['done'] == True:
                completed_advs.add(adv)
        return completed_advs
    
    def check_items(self, curr_advancements):
        completed_items = set()
        for item, adv in self.items_list:
            if adv not in curr_advancements:
                continue
            if item in curr_advancements[adv]['criteria']:
                completed_items.add(item)
        return completed_items
    
    def check_adv_directory(self):
        max_completed_advs = set()
        max_completed_items = set()

        for filename in os.listdir(self.adv_folder):
            if not filename.endswith('.json'):
                continue
            with open(os.path.join(self.adv_folder, filename)) as f:
                data = json.load(f)

            completed_adv = self.check_advancements(data)
            completed_items = self.check_items(data)
            
            max_completed_advs = max(max_completed_advs, completed_adv, key=len)
            max_completed_items = max(max_completed_items, completed_items, key=len)
        print(f"Most achievements completed {len(max_completed_advs)}")
        print(f"Most items completed {len(max_completed_items)}")

        return (max_completed_advs, max_completed_items)

    # def get_data(self, filename='advname_to_path.csv'):
    #     advancements_list = []
    #     with open(os.path.join(self.cwd, 'data', filename), mode='r') as f:
    #         reader = csv.reader(f, delimiter='\t')
    #         for row in reader:
    #             advancements_list.append(row[1])
    #     return advancements_list
    
    def get_data(self, filename='item_to_adv.csv'):
        items_list = []
        with open(os.path.join(self.cwd, 'data', filename), mode='r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                items_list.append(row)
        return items_list
    