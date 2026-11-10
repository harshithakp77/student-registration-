# test_validator.py
# runs a set of test cases on validate_contact and on the duplicate logic
# usage:  python test_validator.py

import os
import tempfile
from validator import validate_contact
from loader import load_contacts

# (description, name, phone, email, should_be_valid)
test_cases = [
    # normal values
    ("Normal valid record", "Aarav Sharma", "9876543210", "aarav.sharma@gmail.com", True),
    ("Valid email with subdomain", "Rohan Verma", "7001122334", "rohan.v@yahoo.co.in", True),
    # name
    ("Blank name", "", "9123456780", "noname@gmail.com", False),
    ("Name with only spaces", "    ", "9123456780", "noname@gmail.com", False),
    ("Single character name", "A", "9123456780", "a@gmail.com", True),
    # phone
    ("Phone starts with 5", "Ananya Sen", "5551234567", "ananya.sen@gmail.com", False),
    ("Phone is empty", "Rahul Das", "", "rahul.das@college.edu", False),
    ("Phone has 9 digits", "Test", "987654321", "t@gmail.com", False),
    ("Phone has 11 digits", "Test", "98765432101", "t@gmail.com", False),
    ("Phone has letters", "Test", "98765abcde", "t@gmail.com", False),
    ("Phone has 10 chars with a dash", "Test", "98765-4321", "t@gmail.com", False),
    ("Boundary: phone starts with 6", "Test", "6000000000", "t@gmail.com", True),
    ("Boundary: phone starts with 9", "Test", "9999999999", "t@gmail.com", True),
    ("Boundary: phone 5999999999", "Test", "5999999999", "t@gmail.com", False),
    ("Boundary: phone 0123456789", "Test", "0123456789", "t@gmail.com", False),
    ("Phone with spaces around it", "Test", " 9876543210 ", "t@gmail.com", True),
    # email
    ("Email with two @", "Vikram Singh", "9898989898", "vikram.singh@@gmail.com", False),
    ("Email with no dot in domain", "Arjun Kapoor", "9876501234", "arjun@kapoor", False),
    ("Email with a space", "Aditya Joshi", "7890123456", "aditya joshi@gmail.com", False),
    ("Email ends with @", "Siddharth Rao", "9112233445", "siddharth.rao@", False),
    ("Email with no @", "Test", "9876543210", "testgmail.com", False),
    ("Email nothing before @", "Test", "9876543210", "@gmail.com", False),
    ("Email empty", "Test", "9876543210", "", False),
    ("Email domain starts with dot", "Test", "9876543210", "a@.com", False),
    ("Email domain ends with dot", "Test", "9876543210", "a@gmail.", False),
    ("Boundary: shortest valid email", "Test", "9876543210", "a@b.c", True),
]

passed = 0
failed = 0

print("=" * 78)
print("VALIDATION TEST CASES")
print("=" * 78)
for description, name, phone, email, expected in test_cases:
    is_valid, reason = validate_contact(name, phone, email)
    if is_valid == expected:
        result = "PASS"
        passed = passed + 1
    else:
        result = "FAIL"
        failed = failed + 1
    print("[" + result + "] " + description)
    print("       input    :", repr(name), repr(phone), repr(email))
    print("       expected :", expected, "| got:", is_valid, "-", reason)

# duplicate test - make a small temporary csv
print()
print("=" * 78)
print("DUPLICATE HANDLING TEST")
print("=" * 78)
temp_csv = "name,phone,email\n"
temp_csv += "Student One,9876543210,one@gmail.com\n"
temp_csv += "Student Two,9876543210,two@gmail.com\n"     # same phone as one
temp_csv += "Student Three,9123456789,ONE@gmail.com\n"    # same email as one (different case)
temp_csv += "Student Four,9123456789,four@gmail.com\n"    # fine
temp_file = os.path.join(tempfile.gettempdir(), "dup_test.csv")
f = open(temp_file, "w")
f.write(temp_csv)
f.close()

students, rejected, total_rows = load_contacts(temp_file, show_log=False)
os.remove(temp_file)

checks = [
    ("4 rows were read", total_rows == 4),
    ("2 students accepted", len(students) == 2),
    ("2 rows rejected as duplicates", len(rejected) == 2),
    ("Duplicate phone caught", "phone" in rejected[0]["reason"]),
    ("Duplicate email caught (case ignored)", "email" in rejected[1]["reason"]),
]
for description, ok in checks:
    if ok:
        print("[PASS] " + description)
        passed = passed + 1
    else:
        print("[FAIL] " + description)
        failed = failed + 1

print()
print("=" * 78)
print("Total passed:", passed, "| Total failed:", failed)
print("=" * 78)
