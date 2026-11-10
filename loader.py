# loader.py
# reads contacts.csv, validates every row, removes duplicates
# and writes the clean students to students_clean.csv

import csv
import os
from validator import validate_contact

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
CONTACTS_FILE = os.path.join(BASE_FOLDER, "contacts.csv")
CLEAN_FILE = os.path.join(BASE_FOLDER, "students_clean.csv")


def load_contacts(filename, show_log=True):
    students = []        # list of dictionaries (valid students)
    rejected = []        # list of dictionaries (rejected rows with reason)
    seen_phones = {}     # phone -> name of the student who has it
    seen_emails = {}     # email (lowercase) -> name
    total_rows = 0

    try:
        file = open(filename, newline="", encoding="utf-8")
    except FileNotFoundError:
        print("Error: could not find", filename)
        return students, rejected, total_rows

    reader = csv.DictReader(file)
    for row in reader:
        total_rows = total_rows + 1

        # row.get can give None if the column is missing, so use "or"
        name = (row.get("name") or "").strip()
        phone = (row.get("phone") or "").strip()
        email = (row.get("email") or "").strip()

        is_valid, reason = validate_contact(name, phone, email)

        # duplicate check only for rows that passed validation
        if is_valid:
            if phone in seen_phones:
                is_valid = False
                reason = "Duplicate phone number (already registered to " + seen_phones[phone] + ")"
            elif email.lower() in seen_emails:
                is_valid = False
                reason = "Duplicate email (already registered to " + seen_emails[email.lower()] + ")"

        if is_valid:
            student = {
                "id": len(students) + 1,
                "name": name,
                "phone": phone,
                "email": email,
            }
            students.append(student)
            seen_phones[phone] = name
            seen_emails[email.lower()] = name
        else:
            rejected.append({
                "row": total_rows,
                "name": name,
                "phone": phone,
                "email": email,
                "reason": reason,
            })

    file.close()

    if show_log:
        print_ingestion_log(total_rows, students, rejected)

    return students, rejected, total_rows


def print_ingestion_log(total_rows, students, rejected):
    print("=" * 60)
    print("INGESTION LOG")
    print("=" * 60)
    print("Total rows read     :", total_rows)
    print("Valid rows accepted :", len(students))
    print("Rejected rows       :", len(rejected))
    print("-" * 60)
    if len(rejected) > 0:
        print("Rejected rows and reasons:")
        for r in rejected:
            shown_name = r["name"]
            if shown_name == "":
                shown_name = "(blank)"
            print("  Row", r["row"], "-", shown_name, "|", r["phone"], "|", r["email"])
            print("        Reason:", r["reason"])
    print("=" * 60)


def save_students(students, filename):
    file = open(filename, "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(file, fieldnames=["id", "name", "phone", "email"], lineterminator="\n")
    writer.writeheader()
    for s in students:
        writer.writerow(s)
    file.close()


def read_clean_csv(filename):
    # reads back a previously saved students_clean.csv
    students = []
    file = open(filename, newline="", encoding="utf-8")
    reader = csv.DictReader(file)
    for row in reader:
        students.append({
            "id": int(row["id"]),
            "name": row["name"],
            "phone": row["phone"],
            "email": row["email"],
        })
    file.close()
    return students


if __name__ == "__main__":
    students, rejected, total_rows = load_contacts(CONTACTS_FILE)
    save_students(students, CLEAN_FILE)
    print("Clean records saved to students_clean.csv")
