import requests
import argparse
import os


from helpers.saver import Saver
from helpers.downloader import Downloader
from helpers.migrator import Migrator


def main():
    parser = argparse.ArgumentParser(description="Пример использования argparse")

    # Определение аргументов
    parser.add_argument("dest_path", type=str, help="Destination folder")
    parser.add_argument("owner", type=str, help="Repository owner")
    parser.add_argument("repo", type=str, help="Repository name")

    # Парсинг аргументов
    args = parser.parse_args()
    dest_path = args.dest_path

    attach_saver = Saver(dest_path + "attachments/")
    object_saver = Saver(dest_path)

    token = os.getenv("GITHUB_API_TOKEN")
    if token is None:
        print("Environment variable GITHUB_API_TOKEN required")
        return

    global user_session
    user_session = os.getenv("GITHUB_USER_SESSION")
    if user_session is None:
        print("Environment variable GITHUB_USER_SESSION required")
        return

    downloader = Downloader(token, user_session)

    migrator = Migrator(downloader, object_saver, attach_saver)
    migrator.migrate_repo_issues(args.owner, args.repo)

    attach_saver.save_correspondence_table()

    print("Done")


if __name__ == "__main__":
    main()
