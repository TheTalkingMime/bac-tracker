import gspread, json, csv, os, time
from itertools import chain
import datetime
import traceback
# Functions
def check_advancements(curr, all_advancements):
    completed_advs = set()
    for adv in all_advancements:
        if adv not in curr:
            continue
        if curr[adv]['done'] == True:
            completed_advs.add(adv)
    return completed_advs

def check_items(curr_advancements, items_advs):
    completed_items = set()
    for item, adv in items_advs:
        if adv not in curr_advancements:
            continue
        if item in curr_advancements[adv]['criteria']:
            completed_items.add(item)
    return completed_items

AL = "blazeandcave:bacap/advancement_legend"
ADV_RANGE = "D2:D"
ITEMS_RANGE = "E2:E"
ADV_COMPLETION_COL = "E"
ITEMS_COMPLETION_COL = "C"

items_list = []
advancements_list = []
with open('advname_to_path.csv', mode='r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        advancements_list.append(row[1])
with open('item_to_adv.csv') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        items_list.append(row)

with open('settings.json') as f:
    settings = json.load(f)

gc = gspread.service_account(filename="credentials.json")
sh = gc.open_by_url(settings['spreadsheet-link'])

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

advancementsSheet = sh.worksheet("Advancements")
itemsSheet = sh.worksheet("All Items/Blocks")

adv_ordering = list(chain.from_iterable(advancementsSheet.get(ADV_RANGE)))
adv_mapping = {item:f"{ADV_COMPLETION_COL}{i+2}" for i, item in enumerate(adv_ordering)}

item_ordering = list(chain.from_iterable(itemsSheet.get(ITEMS_RANGE)))
item_mapping = {item:f"{ITEMS_COMPLETION_COL}{i+2}" for i, item in enumerate(item_ordering)}
max_completed_adv = []
max_completed_items = []

try:
    while True:
        max_completed_adv = []
        max_completed_items = []

        # loop through all jsons in advancements directroy
        folder = 'advancements'
        for filename in os.listdir(folder):
            if not filename.endswith('.json'):
                continue

            with open(os.path.join(folder, filename)) as f:
                curr_advancements = json.load(f)

            # Build set of all advs
            completed_adv = check_advancements(curr_advancements, advancements_list)
            completed_items = check_items(curr_advancements, items_list)

            if len(completed_adv) > len(max_completed_adv):
                max_completed_adv = completed_adv
            if len(completed_items) > len(max_completed_items):
                max_completed_items = completed_items

        adv_data = []
        item_data = []

        for adv in list(max_completed_adv):
            if adv not in adv_mapping:
                continue
            adv_data.append({
                'range': adv_mapping[adv],
                'values': [[True]]
            })

        for item in list(max_completed_items):
            if item not in item_mapping:
                print(item)
                continue
            item_data.append({
                'range': item_mapping[item],
                'values': [[True]]
            })

        advancementsSheet.batch_update(adv_data)
        itemsSheet.batch_update(item_data)
        time.sleep(300)
except Exception as e:
    with open(f'logs/{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log', 'w') as f:
        f.write(str(traceback.format_exc()))
