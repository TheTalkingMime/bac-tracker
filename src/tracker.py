import json, csv, os, time
import datetime
import traceback
from advs_monitor import AdvMonitor
from sheets import SheetsManager
from log_monitor import LogMonitor
from website import Website
from pathlib import Path
from scoreboard import Scoreboard

def main():
    settings = load_settings()
    cwd = settings['cwd'] 

    sheets_manager = SheetsManager(settings)
    required_advs = sheets_manager.get_adv_list()

    world_dir = 'E:\\MultiMC\\instances\\1.20.4\.minecraft\\saves\\world (32)\\'

    adv_path = os.path.join(world_dir, 'advancements')
    log_path = os.path.join(world_dir, '..', '..', 'logs', 'latest.log')

    print(f"Tracking: {adv_path}")
    print(f"Tracking: {log_path}")

    adv_tracker = AdvMonitor(adv_path, cwd, required_advs)
    log_tracker = LogMonitor(log_path, adv_tracker.get_data('advname_to_path.csv'))
    scoreboard = Scoreboard(world_dir)
    website = Website(settings)

    refresh_rate = 10
    time_passed = 0
    max_advs = len(adv_tracker.advancements_list)

    start_time = datetime.datetime.now()
    while True:
        force_refresh = False
        warning = None
        new_advs = sheets_manager.update_first_completions(log_tracker.check())
        if time_passed % 30 == 0:
            time_passed = 0
            adv_data, item_data = adv_tracker.check_adv_directory()
            sheets_manager.update_advancement_progress(adv_data)
            sheets_manager.update_item_progress(item_data, 'ITEMS_SHEET')
            force_refresh = True
            warning = scoreboard.check()
        # warnings = scoreboard.check()
        if force_refresh or new_advs > 0:
            adv_count = sheets_manager.get_adv_count()
            website.update(f"{adv_count}/{max_advs}", warning)
            
        # Ensures loop is running on a consistent refresh rate regardless of execution speed
        time_passed += refresh_rate
        next_run = (start_time + datetime.timedelta(seconds=refresh_rate) - datetime.datetime.now()).total_seconds()
        next_run = max(next_run, 0)

        time.sleep(next_run)
        start_time = datetime.datetime.now()



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