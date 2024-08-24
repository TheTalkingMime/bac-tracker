import re
import logging

logger = logging.getLogger(__name__)

class LogMonitor:
    def __init__(self, filepath, adv_list):
        """
        Initializes the log monitor with the path to the log file.

        :param filepath: Path to the log file to monitor.
        """
        self.filepath = filepath
        self.last_position = None
        self.adv_mapping = {adv_name: adv_path for adv_name, adv_path in adv_list}

    def get_new_lines(self):
        """
        Returns all new lines added to the log file since the last time this method was called.
        """
        new_lines = []
        with open(self.filepath, "r", encoding="utf-8") as file:
            if self.last_position is None:
                file.seek(0, 2)
                self.last_position = file.tell()
            else:
                file.seek(self.last_position)

            line = file.readline()
            while line:
                new_lines.append(line.strip())
                line = file.readline()
            self.last_position = file.tell()

        return new_lines

    def parse_logs(self, log_lines):
        """
        Reads through logs and returns a dictionary of advancements created
        """
        phrases = "|".join([
            "made the advancement",
            "reached the goal",
            "found the hidden advancement",
            "completed the challenge",
            "completed the super challenge",
            "completed every advancement in [tT]he .*? tab, earning them the advancement",
            "completed every advancement in BlazeandCave's Advancements Pack, earning them the coveted title of",
            
        ])

        # Just a fun regex that will find a match if someone gets an advancement
        pattern = rf"\[(\d{{2}}:\d{{2}}:\d{{2}})\] \[Render thread\/INFO\]: \[System\] \[CHAT\] (?:(\w+) has (?:{phrases}) \[(.+?)\]"\
            "|(\w+) have unlocked the root of the (.*?) tab"\
            "|Thank (\w+) for downloading\\\\n(.*?) Pack!)"
        pattern = re.compile(pattern)
        oddities = {
            "End": "The End",
            "65 hours of walking": "65"
        }

        advancements = []

        for line in log_lines:
            match = pattern.search(line)
            

            if match:
                timestamp = match.group(1)
                if match.group(3) is not None:
                    player_name = match.group(2)
                    advancement_name = match.group(3)
                elif match.group(4) is not None:
                    player_name = None
                    advancement_name = match.group(5)
                else:
                    player_name = None
                    advancement_name = match.group(7)
  
                if advancement_name in oddities:
                    advancement_name = oddities[advancement_name]

                if advancement_name not in self.adv_mapping:
                    logging.warning(f"{advancement_name} not found in our mappings")
                    continue

                advancements.append(
                    {
                        "timestamp": timestamp,
                        "player": player_name,
                        "advancement": self.adv_mapping[advancement_name],
                    }
                )
                if player_name is None:
                    logging.warning(f"No name found: {line}")
        return advancements

    def check(self):
        return self.parse_logs(self.get_new_lines())
