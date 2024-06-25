import requests
import secrets
import string

class Overlay:
    def __init__(self, settings):
        self.API_KEY = settings.get('API_KEY', self.generate_api_key())
        self.url = f"{settings.get('URL', 'http://127.0.0.1/')}/send"
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def generate_api_key(length=32):
        characters = string.ascii_letters + string.digits
        api_key = ''.join(secrets.choice(characters) for _ in range(length))
        return api_key

    def update(self, adv_data, warning):
        data = {
            'message': adv_data,
            'warning': warning,
            'api_key': self.API_KEY,
            }
        try:
            requests.post(self.url, data=data, headers=self.headers)
            print("Message sent successfully")
        except Exception as e:
            print("Error sending message:", e)