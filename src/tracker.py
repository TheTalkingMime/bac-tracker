import json, csv, os, time
import datetime
import traceback
import sheets
from advs_monitor import AdvMonitor
from sheets import SheetsManager
from pathlib import Path


def main():
    settings = load_settings()
    cwd = settings['cwd']

    sheets_manager = SheetsManager(settings)
    adv_tracker = AdvMonitor(os.path.join(cwd.parent, 'world', 'advancements'), cwd)

    while True:
        adv_data, item_data = adv_tracker.check_adv_directory()     

        sheets_manager.push_to_gsheet(adv_data, 'ADVANCEMENTS_SHEET')
        sheets_manager.push_to_gsheet(item_data, 'ITEMS_SHEET')

        print("Updated sheet")

        time.sleep(300)



def load_settings():
    cwd = Path(__file__).resolve().parent.parent
    with open(os.path.join(cwd, 'settings', 'settings.json')) as f:
        settings = json.load(f)
    settings['cwd'] = cwd
    return settings


try:
    main()

except Exception as e:
    with open(f'logs/{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log', 'w') as f:
        f.write(str(traceback.format_exc()))