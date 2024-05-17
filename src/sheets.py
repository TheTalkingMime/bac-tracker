import gspread, os, re
from itertools import chain
from player_data import Players
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('google.auth').setLevel(logging.WARNING)
class SheetsManager:
    def __init__(self, settings):
        gc = gspread.service_account(filename= os.path.join(settings['cwd'], 'settings', 'credentials.json'))
        self.conn = gc.open_by_url(settings['spreadsheet-link'])
        self.spreadsheet_format = settings['spreadsheet-format']
        self.sheets_info = {}
        self.player_data = Players()
        
        # Frontload API call to get sheet info and mappings
        self.get_sheet_info('ADVANCEMENTS_SHEET')
        self.get_sheet_info('ITEMS_SHEET')

    
    def update_advancement_progress(self, adv_progress):
        """
        Formats the adv_progress dict for gspread.

        adv_progress format:
        [key] : adv_path (str)
        [0] : % complete (float)
        [1] : Fraction representation of progress (str)
        [2] : Incomplete criteria, if applicable (str)
        [3] : Is adv complete (bool)
        [4] : Player UUID (str)
        """

        
        sheet_info = self.get_sheet_info('ADVANCEMENTS_SHEET')
        sheet_format = sheet_info['format']
        mapping = sheet_info['mapping']

        sheet_data = []
        count = 0
        
        print(len(adv_progress))

        for adv in adv_progress:
            info = adv_progress[adv]
            index = mapping[adv]            
            
            row_data = [{
                'range': self.calc_cell(sheet_format['progress_range'], index),
                'values': [[info[1]]]
            },
            {
                'range': self.calc_cell(sheet_format['incomplete_range'], index),
                'values': [[info[2]]]
            },
            {
                'range': self.calc_cell(sheet_format['status_range'], index),
                'values': [[info[3]]]
            }]
            if info[4] is not None:
                row_data.extend([{
                    'range': self.calc_cell(sheet_format['who_range'], index),
                    'values': [[self.get_face(info[4])]]
                }]) 
            sheet_data.extend(row_data)
        sheet_info['worksheet'].batch_update(sheet_data, value_input_option='USER_ENTERED')


    
   
    def update_first_completions(self, log_data):
        """
        Handles log data. Updates the who, when, and progress column and formats it to gspread.
        """
        sheet_info = self.get_sheet_info('ADVANCEMENTS_SHEET')
        sheet_format = sheet_info['format']

        sheet_data = []
        for completion in log_data:
            timestamp = completion['timestamp']
            player = completion['player']
            advancement = completion['advancement']
            mapping = sheet_info['mapping']
            if advancement not in mapping:
                logging.warning(f"Unmapped advancement: {advancement}")
                continue
            index = mapping[advancement]

            row_data = [{
                'range': self.calc_cell(sheet_format['status_range'], index),
                'values': [[True]]
            },
            {
                'range': self.calc_cell(sheet_format['when_range'], index),
                'values': [[timestamp]]
            }]
            if player is None:
                logging.warning(f"No player data found for {advancement}")
            else:
                row_data.append({
                    'range': self.calc_cell(sheet_format['who_range'], index),
                    'values': [[self.get_face(player)]]
                })
            sheet_data.extend(row_data)
        new_advs = int(len(sheet_data)/3)
        logging.debug(f"Updating spreadsheet... adding {new_advs} amounts of data")
        sheet_info['worksheet'].batch_update(sheet_data, value_input_option='USER_ENTERED')
        return new_advs

    

    def update_item_progress(self, item_progress):
        max_uuid, overall_progress = item_progress
        sheet_info = self.get_sheet_info('ITEMS_SHEET')
        sheet_format = sheet_info['format']
        mapping = sheet_info['mapping']


        sheet_data = []
        for item, uuid in overall_progress.items():
            completed = (uuid == max_uuid)
            index = mapping[item]

            row_data = [{
                'range': self.calc_cell(sheet_format['status_range'], index),
                'values': [[completed]]
            },
            {
                'range': self.calc_cell(sheet_format['who_range'], index),
                'values': [[self.get_face(uuid)]]
            }]
            sheet_data.extend(row_data)
        sheet_info['worksheet'].batch_update(sheet_data, value_input_option='USER_ENTERED')




    def get_adv_count(self):
        sheet_info = self.get_sheet_info('ADVANCEMENTS_SHEET')
        worksheet = sheet_info['worksheet']
        statuses = worksheet.get(sheet_info['format']['status_range'])
        count = 0
        for x in statuses:
            if x == ['TRUE']:
                count += 1
        return count
    
    def get_mapping(self, worksheet, sheet_format):
        ordering = list(chain.from_iterable(worksheet.get(sheet_format['id_range'])))
        mapping = {item: i for i, item in enumerate(ordering)}
        return mapping
    
    def calc_cell(self, range, index:int):
        col, row = re.match("^([A-Za-z]+)(\d+)", range).groups()
        return f"{col}{str(int(row)+index)}"

    def get_face(self, player_name):
        face_url = self.player_data.get_face_url(player_name)
        return f'=IMAGE("{face_url}")'

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
    
    def get_adv_list(self):
        sheet_mapping = self.sheets_info['ADVANCEMENTS_SHEET']['mapping']
        return list(sheet_mapping.keys())
        
