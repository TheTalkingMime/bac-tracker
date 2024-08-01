import json, os, time, datetime, traceback
from sheets import SheetsManager
from pathlib import Path
import tracker_utils as utils
from logging_config import LOGGING_CONFIG
import logging

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def main():
    settings = load_settings()
    cwd = settings['cwd'] 


    world_dir = settings['path_to_world']

    adv_path = os.path.join(world_dir, 'advancements')
    log_path = os.path.join(world_dir, '..', '..', 'logs', 'latest.log')

    sheets_manager = utils.get_SheetsManager(settings)
    required_advs = sheets_manager.get_adv_list()

    adv_tracker = utils.get_AdvMonitor(settings, adv_path, cwd, required_advs)
    log_tracker = utils.get_LogMonitor(settings, log_path, adv_tracker.get_data('advname_to_path.csv'))
    scoreboard = utils.get_Scoreboard(settings)
    overlay = utils.get_Overlay(settings)

    

    refresh_rate = 300
    save_time = 300
    time_passed = 0
    max_advs = len(adv_tracker.advancements_list)

    start_time = datetime.datetime.now()
    while True:
        force_refresh = False
        warning = '-1'
        log_output = utils.check_logs(log_tracker)
        new_advs = utils.update_first_completions(sheets_manager, log_output)
        if time_passed / save_time >= 0:
            logger.info("Checking Advancement file")
            time_passed = 0
            adv_data, item_data = utils.check_adv_directory(adv_tracker)
            
            utils.update_advancement_progress(sheets_manager, adv_data)
            utils.update_item_progress(sheets_manager, item_data)
            force_refresh = True
            warning = scoreboard.check()

        if force_refresh or (new_advs is not None and new_advs > 0):
            adv_count = utils.get_adv_count(sheets_manager)
            utils.update_overlay(overlay, f"{adv_count}/{max_advs}", warning)
            
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