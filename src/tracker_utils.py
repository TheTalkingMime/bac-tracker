from advs_monitor import AdvMonitor
from sheets import SheetsManager
from log_monitor import LogMonitor
from stats import Statistics
from overlay import Overlay
from scoreboard import Scoreboard
from logging_config import LOGGING_CONFIG, log_function_call
import logging

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)



@log_function_call
def get_AdvMonitor(settings, adv_path, cwd, required_advs):
    if not settings['adv_enabled']:
        return None
    adv_tracker = AdvMonitor(adv_path, cwd, required_advs)
    print(f"Tracking: {adv_path}")
    return adv_tracker

@log_function_call
def get_LogMonitor(settings, log_path, adv_list):
    logger.debug("get_LogMonitor()")
    if not settings['log_enabled']:
        return None
    log_tracker = LogMonitor(log_path, adv_list)
    print(f"Tracking: {log_path}")
    return log_tracker

@log_function_call
def get_Scoreboard(settings, cwd):
    logger.debug("get_Scoreboard()")
    if not settings['scoreboard_enabled']:
        return None
    return Scoreboard(settings['path_to_world'], cwd)

def get_Statistics(settings, cwd):
    if not settings["statistics_enabled"]:
        return None
    return Statistics(settings['path_to_world'], cwd)


@log_function_call
def get_SheetsManager(settings):
    if not settings['sheets_enabled']:
        return None
    return SheetsManager(settings)

@log_function_call
def get_Overlay(settings):
    if not settings['overlay_enabled']:
        return None
    return Overlay(settings, settings.get("website_enabled", "localhost"))

#
# Read files
#

@log_function_call
def update_overlay(overlay, message, warning):
    if overlay:
        return overlay.update(message, warning)

@log_function_call
def get_adv_count(sheets_manager):
    if sheets_manager:
        return sheets_manager.get_adv_count()

@log_function_call
def check_adv_directory(adv_tracker):
    if adv_tracker:
        return adv_tracker.check_adv_directory()
    logger.info("adv_tracker is None, skipping...")

@log_function_call
def check_logs(log_tracker):
    if log_tracker:
        return log_tracker.check()

@log_function_call
def check_stats(stat_tracker):
    if stat_tracker:
        return stat_tracker.check()

# Update spreadsheet calls

@log_function_call     
def update_first_completions(sheets_manager, log_output):
    if not (log_output is None or sheets_manager is None):
        return sheets_manager.update_first_completions(log_output)

@log_function_call
def check_scoreboard(scoreboard):
    if scoreboard:
        return scoreboard.check()
  
@log_function_call  
def update_advancement_progress(sheets_manager, adv_data):
    if sheets_manager and adv_data:
        return sheets_manager.update_advancement_progress(adv_data)
    else:
        logger.info("Sheets_manager or adv_data is None, skipping")

@log_function_call
def update_item_progress(sheets_manager, item_data):
    if sheets_manager and item_data:
        return sheets_manager.update_item_progress(item_data)
    
@log_function_call
def update_stat_progress(sheets_manager, stats_data, scoreboard_data):
    if sheets_manager:
        return sheets_manager.update_stat_progress(stats_data, scoreboard_data)