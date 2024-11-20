import json, os, time, datetime, sys
from pathlib import Path
import tracker_utils
from logging_config import *
import logging
import logging.config

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def main():
    logger.info("Program Started!")

    settings = load_settings()
    logger.info("Loaded Settings!")

    cwd = settings['cwd'] 

    world_dir = settings['path_to_world']

    adv_path = os.path.join(world_dir, 'advancements')
    log_path = os.path.join(world_dir, '..', '..', 'logs', 'latest.log')

    sheets_manager = tracker_utils.get_SheetsManager(settings)
    required_advs = sheets_manager.get_adv_list()

    adv_tracker = tracker_utils.get_AdvMonitor(settings, adv_path, cwd, required_advs)
    log_tracker = tracker_utils.get_LogMonitor(settings, log_path, adv_tracker.get_data('advname_to_path.csv'))
    scoreboard = tracker_utils.get_Scoreboard(settings, cwd)
    statistics = tracker_utils.get_Statistics(settings, cwd)
    overlay = tracker_utils.get_Overlay(settings)
    local_output = tracker_utils.get_local_output(settings, cwd)

    refresh_rate = settings['refresh_rate']
    save_rate = 300
    time_passed = 0
    max_advs = len(adv_tracker.advancements_list)

    logger.info(f"Refresh Rate: {refresh_rate}\nSave Time: {save_rate}\nMax Advs: {max_advs}" )

    start_time = datetime.datetime.now()
    logger.info("Setup complete, entering main loop")
    while True:
        force_refresh = False 
        warning = '-1'
        log_output = tracker_utils.check_logs(log_tracker)
        new_advs = tracker_utils.update_first_completions(sheets_manager, log_output)
        if time_passed / save_rate >= 0:
            logger.info("Checking Advancement file")
            time_passed = 0
            adv_data, item_data = tracker_utils.check_adv_directory(adv_tracker)
            stats_data = tracker_utils.check_stats(statistics)
            warning, scoreboard_data, completer_data = tracker_utils.check_scoreboard(scoreboard)
            
            tracker_utils.update_advancement_progress(sheets_manager, adv_data, completer_data)
            tracker_utils.update_local_output(local_output, adv_data)
            tracker_utils.update_item_progress(sheets_manager, item_data)
            tracker_utils.update_stat_progress(sheets_manager, stats_data, scoreboard_data)
            force_refresh = True

        if force_refresh or (new_advs is not None and new_advs > 0):
            adv_count = tracker_utils.get_adv_count(sheets_manager)
            tracker_utils.update_overlay(overlay, f"{adv_count}/{max_advs}", warning)

            
        # Ensures loop is running on a consistent refresh rate regardless of execution speed
        time_passed += refresh_rate
        next_run = (start_time + datetime.timedelta(seconds=refresh_rate) - datetime.datetime.now()).total_seconds()
        next_run = max(next_run, 0)

        time.sleep(next_run)
        start_time = datetime.datetime.now()



def load_settings():
    if getattr(sys, 'frozen', False):
        cwd = Path(sys.argv[0]).resolve().parent
        logger.debug("Running as .exe")
    else:
        cwd = Path(__file__).resolve().parent.parent
        logger.debug("Running as .py")

    logger.debug(f"Running in {cwd}")
    with open(os.path.join(cwd, 'settings', 'settings.json')) as f:
        settings = json.load(f)
    settings['cwd'] = cwd
    return settings


try:
    main()
except Exception as e:
    logger.error(e, exc_info=True)
    input("Send latest.log for debugging")
