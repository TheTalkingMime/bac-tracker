import requests
import secrets
import string
import logging

logger = logging.getLogger(__name__)

class Overlay:
    def __init__(self, settings, is_website):
        self.is_website = is_website
        if self.is_website:
            self.API_KEY = settings.get('API_KEY', self.generate_api_key())
            self.url = f"{settings.get('URL', 'http://127.0.0.1/')}"
            self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def generate_api_key(self, length=32):
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
            requests.post(f"{self.url}/send", data=data, headers=self.headers)
            print("Message sent successfully")
        except Exception as e:
            print("Error sending message:", e)
