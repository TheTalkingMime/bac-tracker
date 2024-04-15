import json, csv, os, time
import datetime
import traceback
from advs_monitor import AdvMonitor
from sheets import SheetsManager
from log_monitor import LogMonitor
from pathlib import Path


def main():
    settings = load_settings()
    cwd = settings['cwd'] 

    sheets_manager = SheetsManager(settings)
    adv_tracker = AdvMonitor(os.path.join(cwd.parent, 'world', 'advancements'), cwd)
    log_tracker = LogMonitor('E:\\MultiMC\\instances\\1.20.4\\.minecraft\\logs\\latest.log', adv_tracker.advancements_list)

    refresh_rate = 10
    time_passed = 0
    while True:
        if time_passed % 300 == 0:
            adv_data, item_data = adv_tracker.check_adv_directory()     
            sheets_manager.update_progress(adv_data, 'ADVANCEMENTS_SHEET')
            sheets_manager.update_progress(item_data, 'ITEMS_SHEET')
        
        sheets_manager.update_first_completions(log_tracker.check())

        time_passed += refresh_rate
        time.sleep(refresh_rate)



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