import PyPDF2
import csv
import os

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        return " ".join(page.extract_text() for page in reader.pages)


def save_resume_to_csv(file_id, resume_content):
    csv_file = "resumes.csv"
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["file_id", "resume_content"])
        writer.writerow([file_id, resume_content])


def get_resume_content(file_id):
    csv_file = "resumes.csv"
    if not os.path.isfile(csv_file):
        return None

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["file_id"] == file_id:
                return row["resume_content"]
    return None