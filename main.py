# main.py
# menu driven console for managing student records

import os
from validator import validate_contact
from loader import load_contacts, save_students, read_clean_csv, CONTACTS_FILE, CLEAN_FILE
from analytics import show_report


def print_table(student_list):
    if len(student_list) == 0:
        print("No students to show.")
        return
    print("-" * 76)
    print("ID".ljust(5) + "Name".ljust(22) + "Phone".ljust(14) + "Email".ljust(35))
    print("-" * 76)
    for s in student_list:
        print(str(s["id"]).ljust(5) + s["name"].ljust(22) + s["phone"].ljust(14) + s["email"].ljust(35))
    print("-" * 76)
    print("Total:", len(student_list))


def get_next_id(students):
    biggest = 0
    for s in students:
        if s["id"] > biggest:
            biggest = s["id"]
    return biggest + 1


def find_duplicate(students, phone, email, skip_id=None):
    # returns a message if phone/email is already used, else empty string
    for s in students:
        if s["id"] == skip_id:
            continue
        if s["phone"] == phone:
            return "Duplicate phone number (already registered to " + s["name"] + ")"
        if s["email"].lower() == email.lower():
            return "Duplicate email (already registered to " + s["name"] + ")"
    return ""


def find_by_id_or_phone(students, key):
    key = key.strip()
    for s in students:
        if str(s["id"]) == key or s["phone"] == key:
            return s
    return None


def search_students(students, keyword):
    keyword = keyword.strip().lower()
    found = []
    if keyword == "":
        return found
    for s in students:
        if keyword == s["phone"]:
            found.append(s)
        elif keyword == s["email"].lower():
            found.append(s)
        elif keyword in s["name"].lower():
            found.append(s)
    return found


# ---------------- menu options ----------------

def view_all(students):
    print("\n--- ALL REGISTERED STUDENTS ---")
    print_table(students)


def search_record(students):
    print("\n--- SEARCH STUDENT ---")
    keyword = input("Enter phone number, email or name: ")
    found = search_students(students, keyword)
    if len(found) == 0:
        print("No student found for '" + keyword.strip() + "'.")
    else:
        print_table(found)


def register_student(students):
    print("\n--- REGISTER NEW STUDENT ---")
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()
    email = input("Enter email: ").strip()

    is_valid, reason = validate_contact(name, phone, email)
    if not is_valid:
        print("Registration failed:", reason)
        return

    duplicate_message = find_duplicate(students, phone, email)
    if duplicate_message != "":
        print("Registration failed:", duplicate_message)
        return

    student = {"id": get_next_id(students), "name": name, "phone": phone, "email": email}
    students.append(student)
    print("Student registered successfully with ID", student["id"])


def update_student(students):
    print("\n--- UPDATE STUDENT ---")
    key = input("Enter student ID or phone number: ")
    student = find_by_id_or_phone(students, key)
    if student is None:
        print("Student not found.")
        return

    print("Current record:")
    print_table([student])
    print("Press Enter to keep the old value.")

    new_name = input("New name: ").strip()
    new_phone = input("New phone: ").strip()
    new_email = input("New email: ").strip()

    if new_name == "":
        new_name = student["name"]
    if new_phone == "":
        new_phone = student["phone"]
    if new_email == "":
        new_email = student["email"]

    is_valid, reason = validate_contact(new_name, new_phone, new_email)
    if not is_valid:
        print("Update failed:", reason)
        return

    duplicate_message = find_duplicate(students, new_phone, new_email, student["id"])
    if duplicate_message != "":
        print("Update failed:", duplicate_message)
        return

    student["name"] = new_name
    student["phone"] = new_phone
    student["email"] = new_email
    print("Student updated successfully.")


def delete_student(students):
    print("\n--- DELETE STUDENT ---")
    key = input("Enter student ID or phone number: ")
    student = find_by_id_or_phone(students, key)
    if student is None:
        print("Student not found.")
        return

    print_table([student])
    answer = input("Are you sure you want to delete this record? (y/n): ").strip().lower()
    if answer == "y":
        students.remove(student)
        print("Student deleted.")
    else:
        print("Delete cancelled.")


def show_menu():
    print("\n==============================================")
    print("   STUDENT REGISTRATION & CONTACT SYSTEM")
    print("==============================================")
    print("1. View All Students")
    print("2. Search Record")
    print("3. Register Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Analytics Report")
    print("7. Exit")


def main():
    # step 1 - read contacts.csv and show the ingestion log
    students, rejected, total_rows = load_contacts(CONTACTS_FILE)

    # step 2 - if we saved our work earlier, continue from that file
    if os.path.exists(CLEAN_FILE):
        students = read_clean_csv(CLEAN_FILE)
        print("Loaded", len(students), "students from students_clean.csv")
    else:
        save_students(students, CLEAN_FILE)

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            view_all(students)
        elif choice == "2":
            search_record(students)
        elif choice == "3":
            register_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            show_report(students, rejected, total_rows)
        elif choice == "7":
            save_students(students, CLEAN_FILE)
            print("Data saved to students_clean.csv. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
