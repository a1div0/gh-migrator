import time
import requests
import subprocess
import os
import shutil

class Downloader:
    def __init__(self, token, user_session):
        self.retry_sleep = 10
        self.retry_timeout = 300
        self.token = token
        self.cookies = {
            "user_session": user_session
        }
        self.session = requests.Session()
        self.session.max_redirects = 3
        self.timeout = 60

    def download_object(self, url):
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

        i = 0
        while i < self.retry_timeout:
            try:
                response = self.session.get(url, headers=headers, cookies=self.cookies, timeout=self.timeout)
                if response.status_code == 200:
                    return response
            except:
                print("")

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
            response = self.session.get(url, headers=headers, cookies=self.cookies, timeout=self.timeout)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except:
            return None

    def download_project_info(self, issue_number, owner, repo):
        url = "https://api.github.com/graphql"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        query = f"""
        {{
          repository(owner: "{owner}", name: "{repo}") {{
            issue(number: {issue_number}) {{
              id
              projectItems(first: 10) {{
                nodes {{
                  id
                  project {{
                    id
                    title
                  }}
                  fieldValues(first: 25) {{
                    nodes {{
                      __typename
                      ... on ProjectV2ItemFieldSingleSelectValue {{
                        field {{
                          ... on ProjectV2FieldCommon {{
                            name
                          }}
                        }}
                        name
                      }}
                      ... on ProjectV2ItemFieldTextValue {{
                        field {{
                          ... on ProjectV2FieldCommon {{
                            name
                          }}
                        }}
                        text
                      }}
                      ... on ProjectV2ItemFieldNumberValue {{
                        field {{
                          ... on ProjectV2FieldCommon {{
                            name
                          }}
                        }}
                        number
                      }}
                      ... on ProjectV2ItemFieldDateValue {{
                        field {{
                          ... on ProjectV2FieldCommon {{
                            name
                          }}
                        }}
                        date
                      }}
                      ... on ProjectV2ItemFieldIterationValue {{
                        field {{
                          ... on ProjectV2FieldCommon {{
                            name
                          }}
                        }}
                        iterationId
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """

        i = 0
        while i < self.retry_timeout:
            try:
                response = self.session.post(url, json={'query': query}, headers=headers, timeout=self.timeout)
                if response.status_code == 200:
                    return response
            except:
                print("")

            i += self.retry_sleep
            print("Get retry...")
            time.sleep(self.retry_sleep)

        raise "Что-то пошло не так... TODO"

    def download_repo_zip(self, owner, repo):
        url = f'https://api.github.com/repos/{owner}/{repo}/zipball'
        headers = {
            "Authorization": f"token {self.token}"
        }

        i = 0
        while i < self.retry_timeout:
            try:
                response = requests.get(url, headers=headers, stream=True)
                if response.status_code == 200:
                    return response
            except:
                print("")

            i += self.retry_sleep
            print("Get retry...")
            time.sleep(self.retry_sleep)

        raise "Что-то пошло не так... TODO"

    def download_repo_zip_v2(self, work_dir, owner, repo):
        temp_dir = work_dir + "temp_repo/"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        repo_url = f"https://{self.token}@github.com/{owner}/{repo}.git"

        # Формируем команду для клонирования репозитория
        clone_command = [
            "git", "clone", repo_url, temp_dir
        ]

        # Выполняем команду клонирования
        result = subprocess.run(clone_command, check=True)
        if result.returncode != 0:
            raise "Что-то пошло не так... TODO"

        # Создаем архив из клонированного репозитория
        archive_name = work_dir + "repo"
        shutil.make_archive(archive_name, 'zip', temp_dir)

        # Удаляем временную директорию
        shutil.rmtree(temp_dir)