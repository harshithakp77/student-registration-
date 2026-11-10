# validator.py
# checks one contact (name, phone, email)
# returns (is_valid, reason) so the loader can log why a row was rejected


def validate_contact(name, phone, email):
    # remove extra spaces from both ends first
    name = name.strip()
    phone = phone.strip()
    email = email.strip()

    # CHECK 1 - name must not be blank
    if len(name) == 0:
        return False, "Name is blank"

    # CHECK 2 - phone
    if len(phone) == 0:
        return False, "Phone number is missing"
    if len(phone) != 10:
        return False, "Phone must be exactly 10 digits"
    if not phone.isdigit():
        return False, "Phone must contain digits only"
    if phone[0] not in "6789":
        return False, "Phone must start with 6, 7, 8 or 9"

    # CHECK 3 - email
    if len(email) == 0:
        return False, "Email is missing"

    for ch in email:
        if ch.isspace():
            return False, "Email must not contain spaces"

    if email.count("@") == 0:
        return False, "Email has no @ symbol"
    if email.count("@") > 1:
        return False, "Email has multiple @ symbols"

    parts = email.split("@")
    before_at = parts[0]
    domain = parts[1]

    if len(before_at) == 0:
        return False, "Email has no characters before @"

    # domain needs a period and it can't be the first or last character
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False, "Email domain must have a period in the middle (like gmail.com)"

    return True, "Valid"
