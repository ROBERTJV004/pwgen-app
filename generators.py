import random
import string


def check_strength(password):
    """Check password strength based on length"""
    if len(password) < 6:
        return "Weak"
    elif len(password) < 10:
        return "Medium"
    else:
        return "Strong"


def generate_password(length, include_numbers, include_symbols):
    """Generate a random password based on user preferences"""
    password = ""
    chars = string.ascii_letters
    if include_numbers:
        chars += string.digits
    if include_symbols:
        chars += string.punctuation
    for i in range(length):
        password += random.choice(chars)
    return password
