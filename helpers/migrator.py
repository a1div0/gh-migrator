import re
import json

def extract_attachments_info(text):
    if text is None:
        return []

    pattern = re.compile(r"\[([^\]]+)\]\((https?://[^\)]+)\)")
    return pattern.findall(text)

def convert_project_info(github_project_info):
    # Инициализация результирующего словаря
    result = {}
    project_items = None

    # Проверка наличия необходимых ключей в JSON-данных
    try:
        if github_project_info['data'] is not None and github_project_info['data']['repository'] is not None:
            repository = github_project_info['data']['repository']
            if repository['issue'] is not None and repository['issue']['projectItems'] is not None:
                project_items = repository['issue']['projectItems']['nodes']
    except:
        return result

    if project_items is None:
        return result

    field_values = None

    try:
        for item in project_items:
            if item['project']['title'] == 'MFactory':
                field_values = item['fieldValues']['nodes']
                break
    except:
        return result

    if field_values is None:
        return result

    for field in field_values:
        try:
            field_name = field.get('field', {}).get('name')
            if field_name == 'Status':
                result['status'] = field['name']
            elif field_name == 'Спринт':
                result['sprint'] = field['date']
            elif field_name == 'План ч':
                result['planned_h'] = field['number']
            elif field_name == 'Затрачено ч':
                result['fact_h'] = field['number']
            elif field_name == 'Start date':
                result['start_date'] = field['date']
            elif field_name == 'Target date':
                result['target_date'] = field['date']
            elif field_name == 'Quarter':
                result['quarter'] = field['name']
            elif field_name == 'Estimate':
                result['estimate'] = field['number']
        except:
            print("")

    return result

class Migrator:
    def __init__(self, downloader, object_saver, attach_saver):
        self.downloader = downloader
        self.object_saver = object_saver
        self.attach_saver = attach_saver

    def migrate_issue(self, issue_number, owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
        response = self.downloader.download_object(url)
        issue = response.json()

        response = self.downloader.download_project_info(issue_number, owner, repo)
        github_project_info = response.json()
        project_info = convert_project_info(github_project_info)
        issue["project_info"] = project_info
        issue_text = json.dumps(issue, ensure_ascii=False)

        self.object_saver.save_object(f"issue-{issue_number}.json", issue_text)

        return issue

    def migrate_comments(self, issue_number, url):
        response = self.downloader.download_object(url)

        comments = response.json()
        if len(comments) > 0:
            self.object_saver.save_object(f"issue-{issue_number}-comments.json", response.text)

        return comments

    def migrate_attachment(self, declare_filename, url):
        content = self.downloader.download_file(url)
        if content is not None:
            self.attach_saver.save_attach(declare_filename, url, content)

    def migrate_attachments(self, attachments_info):
        for attachment_info in attachments_info:
            declare_filename = attachment_info[0]
            url = attachment_info[1]
            self.migrate_attachment(declare_filename, url)

    def migrate_issue_tree(self, issue_number, owner, repo):
        issue = self.migrate_issue(issue_number, owner, repo)
        comments = self.migrate_comments(issue_number, issue["comments_url"])
        attachments_info = extract_attachments_info(issue["body"])

        for comment in comments:
            attachments_info = attachments_info + extract_attachments_info(comment["body"])

        self.migrate_attachments(attachments_info)
        print(f"Issue {issue_number} saved")

    def migrate_repo_issues(self, owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        response = self.downloader.download_object(url)
        issues = response.json()

        if len(issues) == 0:
            print("Repo not contain Issues")
            return

        last_number = issues[0]["number"]

        # Загружаем Issue
        for reduced_number in range(last_number):
            issue_number = reduced_number + 1
            self.migrate_issue_tree(issue_number, owner, repo)

    def migrate_repo(self, owner, repo):
        response = self.downloader.download_repo_zip_v2(self.object_saver.workdir, owner, repo)

        self.migrate_repo_issues(owner, repo)

