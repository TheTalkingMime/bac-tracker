import json, gspread, os
from pathlib import Path
from itertools import chain

ADV_RANGE = "E2:E"
ITEMS_RANGE = "C2:C"

cwd = Path(__file__).resolve().parent.parent

with open(os.path.join(cwd, "settings", "settings.json")) as f:
    settings = json.load(f)
    
gc = gspread.service_account(filename=os.path.join(cwd, "settings", "credentials.json"))
sh = gc.open_by_url(settings['spreadsheet-link'])

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

advancementsSheet = sh.worksheet("Advancements")
itemsSheet = sh.worksheet("All Items/Blocks")

adv_len = len(list(chain.from_iterable(advancementsSheet.get(ADV_RANGE))))
item_len = len(list(chain.from_iterable(itemsSheet.get(ITEMS_RANGE))))

adv_vals = [[False] for x in range(adv_len)]
item_vals = [[False] for x in range(item_len)]

advancementsSheet.update(adv_vals, ADV_RANGE)
itemsSheet.update(item_vals, ITEMS_RANGE)