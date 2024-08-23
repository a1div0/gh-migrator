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
