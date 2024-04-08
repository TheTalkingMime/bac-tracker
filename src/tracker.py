import json, csv, os, time
import datetime
import traceback
import sheets
from pathlib import Path


def main():
    settings = load_settings()
    spreadsheet_format = settings['spreadsheet-format']
    cwd = settings['cwd']

    items_list = []
    advancements_list = []

    with open(os.path.join(cwd, 'data', 'advname_to_path.csv'), mode='r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            advancements_list.append(row[1])
    with open(os.path.join(cwd, 'data', 'item_to_adv.csv'), mode='r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            items_list.append(row)


    conn = sheets.load_credentials(settings)

    advs_mapping = sheets.get_mappings(conn, 'Advancements', spreadsheet_format)
    items_mapping = sheets.get_mappings(conn, 'All Items/Blocks', spreadsheet_format)

    max_completed_adv = []
    max_completed_items = []

    while True:
        max_completed_adv = []
        max_completed_items = []

        # loop through all jsons in advancements directory
        folder = os.path.join(cwd.parent, 'world', 'advancements')
        for filename in os.listdir(folder):
            if not filename.endswith('.json'):
                continue

            # Folder should be adjacent to the world folder
            with open(os.path.join(folder, filename)) as f:
                indiv_advancement_data = json.load(f)

            # Build set of all completed advancements
            completed_adv = check_advancements(indiv_advancement_data, advancements_list)
            completed_items = check_items(indiv_advancement_data, items_list)

            max_completed_adv = max(max_completed_adv, completed_adv, key=len)
            max_completed_items = max(max_completed_items, completed_items, key=len)

        sheets.push_to_gsheet(conn, max_completed_adv, advs_mapping, spreadsheet_format['ADVANCEMENTS_SHEET'])
        sheets.push_to_gsheet(conn, max_completed_items, items_mapping, spreadsheet_format['ITEMS_SHEET'])

        print("Updated sheet")

        time.sleep(300)



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

def load_settings():
    cwd = Path(__file__).resolve().parent.parent
    with open(cwd/'settings'/'settings.json') as f:
        settings = json.load(f)
    settings['cwd'] = cwd
    return settings


try:
    main()

except Exception as e:
    with open(f'logs/{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log', 'w') as f:
        f.write(str(traceback.format_exc()))