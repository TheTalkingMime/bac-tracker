import requests
import logging

logger = logging.getLogger(__name__)

class Players():
    def __init__(self):
        self.uuid_to_name = {}
        self.name_to_uuid = {}
    
    def get_name(self, uuid):
        if uuid in self.uuid_to_name:
            return self.uuid_to_name[uuid]
        clean_uuid = uuid.replace("-", "")
        url = f"https://sessionserver.mojang.com/session/minecraft/profile/{clean_uuid}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data['name']
        else:
            return None
    
    def get_uuid(self, name):
        if name in self.name_to_uuid:
            return self.name_to_uuid[name]
        url = f"https://api.mojang.com/users/profiles/minecraft/{name}"

        logging.debug(f"Performing API Call... {name}")
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            uuid = data['id']
            self.update_dicts(name, uuid)
            logging.debug(f"Updating dicts for {name}")
            return uuid
        else:
            return None
        
    def update_dicts(self, name, uuid):
        self.uuid_to_name[uuid] = name
        self.name_to_uuid[name] = uuid
        return

    def get_face_url(self, name):
        if len(name) <= 16:
            uuid = self.get_uuid(name)
        else:
            uuid = name
        return f"https://crafatar.com/avatars/{uuid}?size=16&overlay"