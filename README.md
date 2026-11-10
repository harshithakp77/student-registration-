# Student Registration & Contact Intelligence System

Semester 1 BCA - Python Programming (Section C Research Project)

A pure Python program that reads a raw `contacts.csv` file, removes the bad
records (wrong phone numbers, wrong emails, blank names, duplicates), keeps the
clean student data in lists/dictionaries, lets a coordinator manage the records
from a menu, and prints a small Business Intelligence report.

No external libraries are used. Only `csv` and `os` from the standard library
(plus `tempfile` in the test file).

## Project Structure

```
student_registration/
├── contacts.csv          # raw input file (20 records)
├── students_clean.csv    # output file with valid, non-duplicate students
├── validator.py          # validate_contact(name, phone, email)
├── loader.py             # reads the csv, validates, removes duplicates, saves clean csv
├── analytics.py          # data quality, telecom series and email domain report
├── main.py               # menu driven console application
├── test_validator.py     # test cases (normal, invalid, duplicate, boundary)
├── proof/
│   ├── console_output.txt   # saved run of the full menu program
│   └── test_cases.txt       # output of test_validator.py
└── README.md
```

## How to Run

You need Python 3 installed. No installation of packages is required.

```
git clone <your-repository-link>
cd student_registration

python loader.py          # only runs the ingestion and creates students_clean.csv
python main.py            # starts the menu program
python test_validator.py  # runs all the test cases
```

If `students_clean.csv` already exists, `main.py` continues from it (so your
changes from the last run are kept). To start fresh from `contacts.csv`, delete
`students_clean.csv` or run `python loader.py` again.

## Validation Rules (validator.py)

`validate_contact(name, phone, email)` returns a tuple `(is_valid, reason)`.

| Field | Rule |
|-------|------|
| Name  | must not be blank or only spaces |
| Phone | exactly 10 characters, digits only, must start with 6, 7, 8 or 9 |
| Email | exactly one `@`, no spaces, something before the `@`, and the domain must have a `.` that is not the first or last character |

The checks run in the order name -> phone -> email and the function stops at the
first failure, so the reason shown is the first problem found in that row.

## Duplicate Handling (loader.py)

Two dictionaries (`seen_phones` and `seen_emails`) store what has already been
accepted. Looking up a key in a dictionary is fast, so each row is checked
without looping through the whole student list. Emails are compared in
lowercase so `ONE@gmail.com` and `one@gmail.com` count as the same email.

## Menu Options (main.py)

| Option | What it does |
|--------|--------------|
| 1 | View all students in a table with IDs |
| 2 | Search by phone number, email or name (name can be partial) |
| 3 | Register a new student (validation + duplicate check) |
| 4 | Update name / phone / email of a student (press Enter to keep old value) |
| 5 | Delete a student by ID or phone number (asks for confirmation) |
| 6 | Show the analytics report |
| 7 | Save to `students_clean.csv` and exit |

## Analytics Report (analytics.py)

* Data quality: total rows, valid rows, rejected rows, accuracy % and a count of
  each error type (Invalid Phone, Bad Email, Missing Name, Duplicate Entry)
* Telecom network breakdown: how many students have phone numbers starting
  with 9, 8, 7 and 6
* Email domain breakdown: how many students use each domain, highest first

The counts are made with dictionary counters like
`counts[domain] = counts.get(domain, 0) + 1`.

## Result on the Sample File

```
Total rows read     : 20
Valid rows accepted : 12
Rejected rows       : 8
Accuracy            : 60.0%
```

Rejected rows: Ananya Sen (phone starts with 5), Rahul Das (phone missing),
Sneha Roy (duplicate phone), blank name row, Vikram Singh (two @), Arjun Kapoor
(no period in domain), Aditya Joshi (space in email), Siddharth Rao (nothing
after @).

## Sample Terminal Session

```
============================================================
INGESTION LOG
============================================================
Total rows read     : 20
Valid rows accepted : 12
Rejected rows       : 8
------------------------------------------------------------
Rejected rows and reasons:
  Row 4 - Ananya Sen | 5551234567 | ananya.sen@gmail.com
        Reason: Phone must start with 6, 7, 8 or 9
  ...

==============================================
   STUDENT REGISTRATION & CONTACT SYSTEM
==============================================
1. View All Students
2. Search Record
3. Register Student
4. Update Student
5. Delete Student
6. Analytics Report
7. Exit
Enter your choice (1-7): 3

--- REGISTER NEW STUDENT ---
Enter name: Test Student
Enter phone: 9000011111
Enter email: test.student@gmail.com
Student registered successfully with ID 13
```

The full session is saved in `proof/console_output.txt`.

## Testing

`test_validator.py` runs 31 checks: normal values, blank name, bad phone
numbers (wrong length, letters, wrong starting digit), bad emails, boundary
values (`6000000000`, `5999999999`, `a@b.c`) and duplicate phone/email rows.
Result: 31 passed, 0 failed (see `proof/test_cases.txt`).

## Notes

* Phone numbers are stored as strings (`str`), not integers, so `.isdigit()` and
  length checks work and nothing gets treated like a number we can add.
* Student IDs are never reused: a new student gets (highest ID + 1).
