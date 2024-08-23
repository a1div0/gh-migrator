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
    parser.add_argument("owner_repo", type=str, help="Repository owner / Repository name")

    # Парсинг аргументов
    args = parser.parse_args()

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

    owner, repo_name = args.owner_repo.split('/')
    dest_path = f"{args.dest_path}/{owner}/{repo_name}/"
    print("------------------------------------------------------")
    print(f"owner = {owner}")
    print(f"repo_name = {repo_name}")
    print(f"dest_path = {dest_path}")

    attach_saver = Saver(dest_path + "attachments/")
    object_saver = Saver(dest_path)
    migrator = Migrator(downloader, object_saver, attach_saver)

    migrator.migrate_repo(owner, repo_name)

    attach_saver.save_correspondence_table()

    print("Done")


if __name__ == "__main__":
    main()
