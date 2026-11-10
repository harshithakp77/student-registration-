# analytics.py
# business intelligence report using only loops and dictionaries


def count_rejection_reasons(rejected):
    counts = {
        "Invalid Phone": 0,
        "Bad Email": 0,
        "Missing Name": 0,
        "Duplicate Entry": 0,
    }
    for r in rejected:
        reason = r["reason"]
        # duplicate reasons also contain the word phone/email, so check them first
        if reason.startswith("Duplicate"):
            counts["Duplicate Entry"] = counts["Duplicate Entry"] + 1
        elif reason.startswith("Name"):
            counts["Missing Name"] = counts["Missing Name"] + 1
        elif reason.startswith("Phone"):
            counts["Invalid Phone"] = counts["Invalid Phone"] + 1
        elif reason.startswith("Email"):
            counts["Bad Email"] = counts["Bad Email"] + 1
    return counts


def count_phone_series(students):
    series = {"9": 0, "8": 0, "7": 0, "6": 0}
    for s in students:
        first_digit = s["phone"][0]
        if first_digit in series:
            series[first_digit] = series[first_digit] + 1
    return series


def count_email_domains(students):
    domains = {}
    for s in students:
        domain = "@" + s["email"].split("@")[1].lower()
        domains[domain] = domains.get(domain, 0) + 1
    return domains


def student_word(n):
    if n == 1:
        return "student"
    return "students"


def show_report(students, rejected, total_rows):
    valid_count = total_rows - len(rejected)
    if total_rows > 0:
        accuracy = (valid_count / total_rows) * 100
    else:
        accuracy = 0.0

    reasons = count_rejection_reasons(rejected)
    series = count_phone_series(students)
    domains = count_email_domains(students)

    line = "=" * 55

    print()
    print(line)
    print("STUDENT REGISTRATION - BUSINESS INTELLIGENCE")
    print(line)
    print("Total Contacts Processed :", total_rows)
    print("Valid Registrations      :", valid_count)
    print("Rejected Records         :", len(rejected))
    print("Data Quality Accuracy    : " + str(round(accuracy, 1)) + "%")
    print("Students In System Now   :", len(students))

    print()
    print("--- Data Entry Errors ---")
    for reason_name in reasons:
        print(reason_name.ljust(26) + ":", reasons[reason_name])

    print()
    print("--- Telecom Network Breakdown ---")
    for digit in ["9", "8", "7", "6"]:
        label = digit + "-Series"
        print(label.ljust(26) + ":", series[digit], student_word(series[digit]))

    print()
    print("--- Top Email Domains ---")
    # sort by count (highest first), then by name
    ranked = sorted(domains.items(), key=lambda item: (-item[1], item[0]))
    for domain, count in ranked:
        print(domain.ljust(26) + ":", count, student_word(count))
    print(line)
