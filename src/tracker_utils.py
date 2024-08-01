from advs_monitor import AdvMonitor
from sheets import SheetsManager
from log_monitor import LogMonitor
from overlay import Overlay
from pathlib import Path
from scoreboard import Scoreboard

def get_AdvMonitor(settings, adv_path, cwd, required_advs):
    if not settings['adv_enabled']:
        return None
    adv_tracker = AdvMonitor(adv_path, cwd, required_advs)
    print(f"Tracking: {adv_path}")
    return adv_tracker

def get_LogMonitor(settings, log_path, adv_list):
    if not settings['log_enabled']:
        return None
    log_tracker = LogMonitor(log_path, adv_list)
    print(f"Tracking: {log_path}")
    return log_tracker

def get_Scoreboard(settings):
    if not settings['scoreboard_enabled']:
        return None
    return Scoreboard(settings['path_to_world'])

def get_SheetsManager(settings):
    if not settings['sheets_enabled']:
        return None
    return SheetsManager(settings)

def get_Overlay(settings):
    if not settings['overlay_enabled']:
        return None
    return Overlay(settings, settings.get("website_enabled", "localhost"))

def update_overlay(overlay, message, warning):
    if overlay:
        return overlay.update(message, warning)

def get_adv_count(sheets_manager):
    if sheets_manager:
        return sheets_manager.get_adv_count()

def check_adv_directory(adv_tracker):
    if adv_tracker:
        return adv_tracker.check_adv_directory()

def check_logs(log_tracker):
    if log_tracker:
        return log_tracker.check()
        
def update_first_completions(sheets_manager, log_output):
    if not (log_output is None or sheets_manager is None):
        return sheets_manager.update_first_completions(log_output)

def check_scoreboard(scoreboard):
    if scoreboard:
        return scoreboard.check()
    
def update_advancement_progress(sheets_manager, adv_data):
    if sheets_manager and adv_data:
        return sheets_manager.update_advancement_progress(adv_data)

def update_item_progress(sheets_manager, item_data):
    if sheets_manager and item_data:
        return sheets_manager.update_item_progress(item_data)