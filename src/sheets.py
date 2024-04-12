import gspread, os
from itertools import chain

class SheetsManager:
    def __init__(self, settings):
        gc = gspread.service_account(filename= os.path.join(settings['cwd'], 'settings', 'credentials.json'))
        self.conn = gc.open_by_url(settings['spreadsheet-link'])

    def format_to_spreadsheet(self, completed_objs, mapping):
        data = []
        for adv in list(completed_objs):
            if adv not in mapping:
                continue
            data.append({
                'range': mapping[adv],
                'values': [[True]]
            })
        return data

    def push_to_gsheet(self, completed_objs, mapping, sheet_name):
        data = self.format_to_spreadsheet(completed_objs, mapping)
        self.conn.worksheet(sheet_name).batch_update(data)

    def get_mappings(self, sheet_name, spreadsheet_format):
        sheet = self.conn.worksheet(sheet_name)
        adv_ordering = list(chain.from_iterable(sheet.get(spreadsheet_format['ADV_RANGE'])))
        adv_mapping = {item:f"{spreadsheet_format['ADV_COMPLETION_COL']}{i+2}" for i, item in enumerate(adv_ordering)}
        return adv_mapping