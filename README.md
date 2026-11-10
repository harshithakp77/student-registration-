Student Registration & Contact Intelligence System


This project is a Registration and Contact Intelligence Engine written completely in core Python. It was built for a regional coaching institute that collects student registration leads in an offline spreadsheet file called `contacts.csv`. The problem with this file is that the data entered into it is often not clean. Some rows have a missing name, some have phone numbers that are too short or start with a wrong digit, some have emails that are not written properly, and some students are entered two times. My program reads this raw file, checks every row, throws away the faulty and repeated records with a clear reason, keeps the good records in Python lists and dictionaries, and then lets a coaching coordinator manage those students from a simple menu in the terminal. It also prepares a small Business Intelligence report which shows how good the data was, which phone number series the students use, and which email providers they prefer.

The whole project uses only the standard Python library (`csv`, `os`, and `tempfile` for the test file). No outside package has to be installed, so it can run on any computer that has Python 3.

 How the Project Is Organised

The project is divided into small files and each file has only one job. This makes the code easy to read, easy to test and easy to reuse. The folder looks like this:

```
student_registration/
├── contacts.csv          raw input file with 20 student records
├── students_clean.csv    output file with valid, non-duplicate students
├── validator.py          the validation function
├── loader.py             reads the csv, validates, removes duplicates, saves
├── analytics.py          the business intelligence report
├── main.py               the menu driven console program
├── test_validator.py     test cases for validation and duplicates
├── proof/
│   ├── console_output.txt    saved run of the full program
│   └── test_cases.txt        saved result of the test file
└── README.md             this file
```

`validator.py` contains the function `validate_contact(name, phone, email)` which checks one student at a time. `loader.py` is the ingestion script which opens `contacts.csv`, sends every row to the validator, removes duplicates and writes the clean data to `students_clean.csv`. `analytics.py` takes the loaded data and counts things using loops and dictionaries to create the report. `main.py` is the file that the user actually runs, and it joins all the other files together with a menu. The `proof` folder keeps evidence that the program was tested, and `test_validator.py` is the script that creates the test evidence.

 How to Run the Project

First, make sure Python 3 is installed by typing `python --version` in the terminal. Then download or clone the repository and open a terminal inside the project folder. To clone it you can use the command below, and then move into the folder.

```
git clone <your-repository-link>
cd student_registration
```

After that there are three commands that can be used. The command `python loader.py` only runs the ingestion step, which reads `contacts.csv`, prints the ingestion log and creates `students_clean.csv`. The command `python main.py` starts the full menu program, which is the main application. The command `python test_validator.py` runs all the test cases and prints which ones passed. On some computers the word `python` may need to be replaced with `python3`.

One thing to know is that when `main.py` starts, it first reads `contacts.csv` and prints the ingestion log. If a file called `students_clean.csv` already exists, the program continues from that saved file, so any students that were added, changed or deleted in the last session are not lost. If you want to start again from the original data, delete `students_clean.csv` or run `python loader.py` again.

 How the Validation Works

The validation is done by the function `validate_contact(name, phone, email)` in `validator.py`. It does not just say yes or no. It returns a tuple `(is_valid, reason)`, so when a row is rejected the loader knows exactly why and can write the reason in the log. The function first removes extra spaces from the start and end of all three values using `.strip()`, and then it runs three checks one after another. If any check fails, the function stops at once and returns `False` with the reason, so the reason always shows the first problem found in that row.

The first check is the name, which must not be blank or made only of spaces. The second check is the phone number, which must be exactly 10 characters long, must contain digits only (checked with `.isdigit()`), and must start with 6, 7, 8 or 9. A missing phone number is reported separately as "Phone number is missing". The third check is the email, which must contain exactly one `@` symbol, must not contain any whitespace, must have some characters before the `@`, and its domain part after the `@` must contain a period that is not the first or the last character. This is why `arjun@kapoor` and `siddharth.rao@` are rejected but `rohan.v@yahoo.co.in` is accepted.

 How Duplicates Are Handled

After a row passes validation, the loader checks whether the same student was already accepted earlier. For this it keeps two dictionaries named `seen_phones` and `seen_emails`. Every time a student is accepted, the phone number and the lowercase email are stored in these dictionaries together with the student's name. When the next row comes, the program only looks up the phone and email in the dictionaries instead of checking the whole student list again, which is much faster because dictionary lookup takes constant time. The emails are changed to lowercase before comparing, so `ONE@gmail.com` and `one@gmail.com` are treated as the same email. In the sample file, Sneha Roy is rejected because her phone number `9876543210` already belongs to Aarav Sharma, and the message in the log even tells whose record it clashed with.

 The Menu Options

When `main.py` runs, a menu with seven options is shown, and the program keeps asking for a choice until the user selects Exit. Option 1 shows all registered students in a neat table with their ID, name, phone and email. Option 2 searches for a student by phone number, email or name, and the name search also works with part of a name and ignores capital letters, so typing `priya` finds Priya Patel. Option 3 registers a new student by asking for the name, phone and email, then applying the same validation and duplicate check before adding the student with a new ID. Option 4 updates an existing student which is found by ID or phone number, and the user can press Enter to keep an old value; the new values go through validation and a duplicate check again, so a record can never be changed into something invalid. Option 5 deletes a student by ID or phone number, and it shows the record and asks for a yes or no confirmation first so that nothing is removed by mistake. Option 6 prints the analytics report. Option 7 saves all the current students to `students_clean.csv` and exits the program. If the user types anything that is not a number from 1 to 7, the program shows a message and shows the menu again instead of crashing. Student IDs are never reused, because a new student always gets the highest existing ID plus one.

 The Analytics Report

The report is made in `analytics.py` using only loops, dictionaries and string operations. The first part is the Data Quality Diagnostic, which shows the total contacts processed, the number of valid and rejected records, the accuracy percentage calculated as valid divided by total multiplied by 100, and a count of each type of error such as Invalid Phone, Bad Email, Missing Name and Duplicate Entry. The second part is the Telecom Network Distribution, which looks at the first digit of every valid phone number and counts how many students belong to the 9, 8, 7 and 6 series. The third part is the Email Domain Breakdown, which takes the part after the `@` of every email, counts how many times each domain appears using the pattern `domains[domain] = domains.get(domain, 0) + 1`, and prints the domains from the most used to the least used. At the end everything is displayed as a neat summary on the console.

 Result on the Sample File

When the 20 rows of `contacts.csv` are processed, 12 rows are accepted and 8 are rejected, so the data quality accuracy is 60.0%. The rejected rows are Ananya Sen (phone starts with 5), Rahul Das (phone number missing), Sneha Roy (duplicate phone number), the row with a blank name, Vikram Singh (two `@` symbols), Arjun Kapoor (no period in the domain), Aditya Joshi (a space inside the email) and Siddharth Rao (nothing after the `@`). In the error breakdown this makes 2 invalid phones, 4 bad emails, 1 missing name and 1 duplicate. Among the 12 valid students, the phone series are 4 students in the 9-series, 4 in the 8-series, 2 in the 7-series and 2 in the 6-series. The most common email domain is `@gmail.com` with 4 students, followed by `@outlook.com` with 3 and `@yahoo.com` with 2.

A small part of the report looks like this:

```
=======================================================
STUDENT REGISTRATION - BUSINESS INTELLIGENCE
=======================================================
Total Contacts Processed : 20
Valid Registrations      : 12
Rejected Records         : 8
Data Quality Accuracy    : 60.0%
```

## Testing

Testing was done with the file `test_validator.py`, which runs 31 checks and prints PASS or FAIL for each one. The checks cover normal valid records, a blank name, a name with only spaces, phone numbers that are too short, too long, contain letters or a dash, and phone numbers that start with a wrong digit. They also cover emails with two `@` symbols, no `@`, spaces, nothing before the `@`, and domains that start or end with a period. Boundary values were tested too, for example the phone numbers `6000000000` and `9999999999` which are valid, `5999999999` and `0123456789` which are not valid, and the shortest valid email `a@b.c`. The duplicate handling is tested by creating a small temporary csv which has a repeated phone number and a repeated email written in capital letters. All 31 checks passed, and the result is saved in `proof/test_cases.txt`. A full run of the menu program, which includes viewing, searching, registering with valid and invalid data, updating, deleting, the analytics report and invalid menu choices, is saved in `proof/console_output.txt`.

Design Decisions

Phone numbers are stored as strings (`str`) and not as integers, because we do not do any arithmetic on them, and a string allows `.isdigit()` and length checks and keeps any leading zeros. The code is divided into separate files so the validation function can be reused by both the loader and the menu program without writing the same checks twice. The program uses `csv.DictReader` so that each column is read by its header name (`name`, `phone`, `email`) instead of a fixed position number, which makes the code easier to understand and safe even if the column order changes.
