import json, gspread, os
from pathlib import Path
from itertools import chain

def get_mapping(worksheet, sheet_format):
    ordering = list(chain.from_iterable(worksheet.get(sheet_format['id_range'])))
    mapping = {item: i for i, item in enumerate(ordering)}
    return mapping

def get_sheet_info(sheet_type, conn):
    sheet_format = settings['spreadsheet-format'][sheet_type]
    worksheet = conn.worksheet(sheet_format['name'])
    # mapping = get_mapping(worksheet, sheet_format)

    return {
        'worksheet': worksheet,
        'format': sheet_format
        # 'mapping': mapping
    }


cwd = Path(__file__).resolve().parent.parent

with open(os.path.join(cwd, "tracker", "settings", "settings.json")) as f:
    settings = json.load(f)
    
gc = gspread.service_account(filename=os.path.join(cwd, "tracker", "settings", "credentials.json"))
conn = gc.open_by_url(settings['spreadsheet-link'])

advancement_sheet_info = get_sheet_info("ADVANCEMENTS_SHEET", conn=conn)
items_sheet_info = get_sheet_info("ITEMS_SHEET", conn=conn)

advancementsSheet = advancement_sheet_info['worksheet']
itemsSheet = items_sheet_info['worksheet']

adv_sheet_format = advancement_sheet_info['format']
items_sheet_format = items_sheet_info['format']

adv_len = len(list(chain.from_iterable(advancementsSheet.get(adv_sheet_format['id_range']))))
item_len = len(list(chain.from_iterable(itemsSheet.get(items_sheet_format['id_range']))))

adv_vals = [{
                'range': adv_sheet_format['status_range'],
                'values': [[False] for x in range(adv_len)]
            },
            {
                'range': adv_sheet_format['who_range'],
                'values': [[""] for x in range(adv_len)]
            },
            {
                'range': adv_sheet_format['when_range'],
                'values': [[""] for x in range(adv_len)]
            },
            {
                'range': adv_sheet_format['progress_range'],
                'values': [[""] for x in range(adv_len)]
            },
            {
                'range': adv_sheet_format['incomplete_range'],
                'values': [[""] for x in range(adv_len)]
            }]

item_vals = [{
                'range': items_sheet_format['status_range'],
                'values': [[False] for x in range(adv_len)]
            },
            {
                'range': items_sheet_format['who_range'],
                'values': [[""] for x in range(adv_len)]
            }]

advancementsSheet.batch_update(adv_vals)
itemsSheet.batch_update(item_vals)