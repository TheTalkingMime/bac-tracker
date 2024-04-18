import requests

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
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data['id']
        else:
            return None
        
    def update_dicts(self, name, uuid):
        self.uuid_to_name[uuid] = name
        self.name_to_uuid[name] = uuid

    def get_face_url(self, name):
        uuid = self.get_uuid(name)
        return f"https://crafatar.com/avatars/{uuid}?size=16&overlay"