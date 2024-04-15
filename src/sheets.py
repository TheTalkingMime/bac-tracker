import gspread, os, re
from itertools import chain

class SheetsManager:
    def __init__(self, settings):
        gc = gspread.service_account(filename= os.path.join(settings['cwd'], 'settings', 'credentials.json'))
        self.conn = gc.open_by_url(settings['spreadsheet-link'])
        self.spreadsheet_format = settings['spreadsheet-format']
        self.sheets_info = {}

    def format_to_spreadsheet(self, completed_objs, sheet_type):
        sheet_info = self.get_sheet_info(sheet_type)
        range = sheet_info['format']['status_range']
        mapping = sheet_info['mapping']

        data = []
        for adv in list(completed_objs):
            if adv not in sheet_info['mapping']:
                continue
            data.append({
                'range': self.get_cell(range, mapping[adv]),
                'values': [[True]]
            })
        return data
    
    """
    Handles log data. Updates the who, when, and progress column.
    """
    def update_first_completions(self, log_data):
        sheet_info = self.get_sheet_info('ADVANCEMENTS_SHEET')
        sheet_format = sheet_info['format']

        data = []
        for completion in log_data:
            timestamp = completion['timestamp']
            player = completion['player']
            advancement = completion['advancement']
            mapping = sheet_info['mapping']
            if advancement not in mapping:
                print(f"Unmapped advancement: {advancement}")
                continue
            index = mapping[advancement]

            data.extend([{
                'range': self.get_cell(sheet_format['status_range'], index),
                'values': [[True]]
            },
            {
                'range': self.get_cell(sheet_format['who_range'], index),
                'values': [[player]]
            },
            {
                'range': self.get_cell(sheet_format['when_range'], index),
                'values': [[timestamp]]
            }])
        print(f"Updating spreadsheet... adding {int(len(data)/3)} amounts of data")
        sheet_info['worksheet'].batch_update(data)
        return data


    def update_progress(self, completed_objs, sheet_type):
        sheet_info = self.get_sheet_info(sheet_type)
        data = self.format_to_spreadsheet(completed_objs, sheet_type)
        sheet_info['worksheet'].batch_update(data)

    def get_mapping(self, worksheet, sheet_format):
        ordering = list(chain.from_iterable(worksheet.get(sheet_format['id_range'])))
        mapping = {item: i for i, item in enumerate(ordering)}
        return mapping
    
    def get_cell(self, range, index):
        col, row = re.match("^([A-Za-z]+)(\d+)", range).groups()
        return f"{col}{row+index}"

    def get_sheet_info(self, sheet_type):
        if sheet_type in self.sheets_info:
            return self.sheets_info[sheet_type]
        
        sheet_format = self.spreadsheet_format[sheet_type]
        worksheet = self.conn.worksheet(sheet_format['name'])
        mapping = self.get_mapping(worksheet, sheet_format)

        self.sheets_info[sheet_type] = {
            'worksheet': worksheet,
            'format': sheet_format,
            'mapping': mapping
        }
        return self.sheets_info[sheet_type]