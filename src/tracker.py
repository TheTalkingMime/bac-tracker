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
    obs = settings['obs-display-capture']['ON']

    sheets_manager = SheetsManager(settings)
    required_advs = sheets_manager.get_adv_list()

    world_dir = settings["path_to_advs"]

    adv_path = os.path.join(world_dir, 'advancements')
    # log_path = os.path.join(world_dir, '..', '..', 'logs', 'latest.log')

    print(f"Tracking: {adv_path}")
    # print(f"Tracking: {log_path}")

    adv_tracker = AdvMonitor(adv_path, cwd, required_advs)
    # log_tracker = LogMonitor(log_path, adv_tracker.get_data('advname_to_path.csv'))
    scoreboard = Scoreboard(world_dir, cwd)
    website = Website(settings)

    refresh_rate = settings["refresh_rate"]
    time_passed = 0
    max_advs = len(adv_tracker.advancements_list)

    start_time = datetime.datetime.now()
    while True:
        force_refresh = obs & False 
        warning = '-1'
        # log_output = log_tracker.check()
        # new_advs = sheets_manager.update_first_completions(log_output)
        if time_passed % 300 == 0:
            print("Checking Advancement file")
            time_passed = 0
            adv_data, item_data = adv_tracker.check_adv_directory()
            warning, scores_data = scoreboard.check()

            sheets_manager.update_advancement_progress(adv_data)
            sheets_manager.update_item_progress(item_data)

            force_refresh = obs & True
            
        # warnings = scoreboard.check()
        if force_refresh:
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