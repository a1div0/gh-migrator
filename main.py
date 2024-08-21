import requests
import argparse
import os
import re

headers = ''

def save_to_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def download_issue(issue_number, owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    # Загружаем сам ишью и пока пишем в файл
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise "Что-то пошло не так... TODO"

    save_to_file(f"database/issue-{issue_number}.json", response.text)

    return response.json()

def download_comments(issue_number, url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise "Что-то пошло не так... TODO"

    comments = response.json()
    if len(comments) > 0:
        save_to_file(f"database/issue-{issue_number}-comments.json", response.text)

    return comments

def download_image(image_url):
    response = requests.get(image_url, headers=headers)
    response.raise_for_status()

    save_filename = "database/images/" + os.path.basename(image_url) + ".png"
    with open(save_filename, 'wb') as file:
        file.write(response.content)

def download_images(image_urls):
    for image_url_with_tags in image_urls:
        image_url = image_url_with_tags[9:-1]
        download_image(image_url)

def image_urls_from_body(body):
    if body is None:
        return []

    pattern = r'!\[image\]\(.*?\)'
    return re.findall(pattern, body)

def migrate_issue(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    # Определяем сколько всего Issue
    response = requests.get(url, headers=headers, params={"state": "all", "per_page": 1})
    if response.status_code != 200:
        raise "Что-то пошло не так... TODO"

    issues = response.json()

    if len(issues) == 0:
        print('Repo not contain Issue')
        return

    last_number = issues[0]['number']

    # Загружаем Issue
    for reduced_number in range(last_number):
        issue_number = reduced_number + 1
        issue = download_issue(issue_number, owner, repo)
        comments = download_comments(issue_number, issue['comments_url'])
        image_urls = image_urls_from_body(issue['body'])

        for comment in comments:
            image_urls = image_urls + image_urls_from_body(comment['body'])

        download_images(image_urls)
        print(f"Issue {issue_number} saved")

def main():
    parser = argparse.ArgumentParser(description="Пример использования argparse")

    # Определение аргументов
    parser.add_argument("owner", type=str, help="Repository owner")
    parser.add_argument("repo", type=str, help="Repository name")

    # Парсинг аргументов
    args = parser.parse_args()
    token = os.getenv("GITHUB_API_TOKEN")

    if token is None:
        print("Environment variable GITHUB_API_TOKEN required")
        return

    global headers
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    migrate_issue(args.owner, args.repo)

    print('Done')

if __name__ == "__main__":
    main()
