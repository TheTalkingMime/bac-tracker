import gspread, os, re
from itertools import chain

class SheetsManager:
    def __init__(self, settings):
        gc = gspread.service_account(filename= os.path.join(settings['cwd'], 'settings', 'credentials.json'))
        self.conn = gc.open_by_url(settings['spreadsheet-link'])
        self.spreadsheet_format = settings['spreadsheet-format']
        self.sheets_info = {}

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

    def push_to_gsheet(self, completed_objs, sheet_type):
        sheet_info = self.get_sheet_info(sheet_type)
        data = self.format_to_spreadsheet(completed_objs, sheet_info['mappings'])
        sheet_info['worksheet'].batch_update(data)

    def get_mapping(self, worksheet, sheet_format):
        ordering = list(chain.from_iterable(worksheet.get(sheet_format['id_range'])))
        status_range_info = self.get_range_info(sheet_format['status_range'])
        mapping = {item:f"{status_range_info[0]}{i+int(status_range_info[1])}" for i, item in enumerate(ordering)}
        return mapping
    
    def get_range_info(self, range):
        range_info = re.match("^([A-Za-z]+)(\d+)", range)
        return range_info.group(1), range_info.group(2)

    def get_sheet_info(self, sheet_type):
        if sheet_type in self.sheets_info:
            return self.sheets_info[sheet_type]
        
        sheet_format = self.spreadsheet_format[sheet_type]
        worksheet = self.conn.worksheet(sheet_format['name'])
        mapping = self.get_mapping(worksheet, sheet_format)

        self.sheets_info[sheet_type] = {
            'worksheet': worksheet,
            'spreadsheet-format': sheet_format,
            'mappings': mapping
        }
        return self.sheets_info[sheet_type]