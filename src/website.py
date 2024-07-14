import requests

class Website:
    def __init__(self, settings):
        self.API_KEY = settings['obs-display-capture']['API_KEY']
        self.url = f"{settings['obs-display-capture']['URL']}/send"
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}


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