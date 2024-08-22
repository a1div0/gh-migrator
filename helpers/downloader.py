import time
import requests

class Downloader:
    def __init__(self, token, user_session):
        self.retry_sleep = 10
        self.retry_timeout = 300
        self.token = token
        self.cookies = {
            "user_session": user_session
        }

    def download_object(self, url):
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

        i = 0
        while i < self.retry_timeout:
            response = requests.get(url, headers=headers, cookies=self.cookies)
            if response.status_code == 200:
                return response

            i += self.retry_sleep
            print("Get retry...")
            time.sleep(self.retry_sleep)

        raise "Что-то пошло не так... TODO"

    def download_file(self, url):
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3.raw"
        }

        try:
            response = requests.get(url, headers=headers, cookies=self.cookies)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except:
            return None
