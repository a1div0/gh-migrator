import os
import csv


def get_file_extension_with_dot(filename):
    if filename == "image":
        return ".png"
    else:
        _, extension = os.path.splitext(filename)
        return extension


class Saver:
    def __init__(self, new_workdir):
        self.correspondence_table = []
        self.workdir = ""
        self.workdir = new_workdir
        os.makedirs(self.workdir, exist_ok=True)

    def save_attach(self, declare_filename, url, content):
        number = len(self.correspondence_table) + 1
        dot_ext = get_file_extension_with_dot(declare_filename)
        save_filename = f"{self.workdir}{number:06}{dot_ext}"

        with open(save_filename, "wb") as file:
            file.write(content)

        self.correspondence_table.append({
            "declare_filename": declare_filename,
            "saved_filename": save_filename,
            "url": url
        })

    def save_object(self, filename, text):
        save_filename = f"{self.workdir}{filename}"
        with open(save_filename, "w", encoding="utf-8") as file:
            file.write(text)

    def save_correspondence_table(self):
        csv_filename = os.path.join(self.workdir, "!correspondence_table.csv")
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["declare_filename", "saved_filename", "url"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.correspondence_table:
                writer.writerow(row)
