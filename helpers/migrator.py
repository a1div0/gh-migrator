import re

def extract_attachments_info(text):
    if text is None:
        return []

    pattern = re.compile(r"\[([^\]]+)\]\((https?://[^\)]+)\)")
    return pattern.findall(text)

class Migrator:
    def __init__(self, downloader, object_saver, attach_saver):
        self.downloader = downloader
        self.object_saver = object_saver
        self.attach_saver = attach_saver

    def migrate_issue(self, issue_number, owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
        response = self.downloader.download_object(url)
        self.object_saver.save_object(f"issue-{issue_number}.json", response.text)

        return response.json()

    def migrate_comments(self, issue_number, url):
        response = self.downloader.download_object(url)
        self.object_saver.save_object(f"issue-{issue_number}.json", response.text)

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

