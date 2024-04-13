import re
import time

class LogMonitor:
    def __init__(self, filepath):
        """
        Initializes the log monitor with the path to the log file.
        
        :param filepath: Path to the log file to monitor.
        """
        self.filepath = filepath
        self.last_position = None

    def get_new_lines(self):
        """
        Returns all new lines added to the log file since the last time this method was called.
        """
        new_lines = []
        with open(self.filepath, 'r', encoding='utf-8') as file:
            # If this is the first call, move to the end of the file
            if self.last_position is None:
                file.seek(0, 2)
                self.last_position = file.tell()
            else:
                # Move to the last known position
                file.seek(self.last_position)
            
            # Read all new lines and update the last known position
            line = file.readline()
            while line:
                new_lines.append(line.strip())
                line = file.readline()
            self.last_position = file.tell()
        
        return new_lines
    
    def parse_logs(self, log_lines):
        
        # Regular expression to match the advancement log line format
        # and capture the timestamp, player name, and advancement
        pattern = re.compile(
            r"\[(\d{2}:\d{2}:\d{2})\] \[Render thread/INFO\]: \[System\] \[CHAT\] (\w+) has made the advancement \[(.+?)\]"
            )
        
        advancements = []

        for line in log_lines:
            match = pattern.search(line)
            if match:
                timestamp, player_name, advancement = match.groups()
                advancements.append({
                    "timestamp": timestamp,
                    "player": player_name,
                    "advancement": advancement
                })
                print(f"{player_name} achieved {advancement} at {timestamp}")
        return advancements
        
    def check_for_advs(self):
        return self.parse_logs(self.get_new_lines())
    
