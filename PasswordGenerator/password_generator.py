# password_generator.py
import random
import string
import argparse


def generate_password(length=12, use_digits=True, use_special_chars=True):
    """
    Generate secure password with customizable length and character types
    """
    letters = string.ascii_letters
    digits = string.digits if use_digits else ""
    special_chars = "!@#$%^&*()_-+=<>?" if use_special_chars else ""

    all_chars = letters + digits + special_chars

    password_chars = []

    if letters:
        password_chars.append(random.choice(letters))
    if use_digits and digits:
        password_chars.append(random.choice(digits))
    if use_special_chars and special_chars:
        password_chars.append(random.choice(special_chars))

    remaining_length = length - len(password_chars)
    if remaining_length > 0:
        password_chars.extend(random.choices(all_chars, k=remaining_length))

    random.shuffle(password_chars)

    return "".join(password_chars)


def calculate_password_strength(password):
    """
    Evaluate password strength based on various criteria
    """
    strength = 0

    if len(password) >= 8:
        strength += 1
    if len(password) >= 12:
        strength += 1
    if len(password) >= 16:
        strength += 1

    if any(char.isdigit() for char in password):
        strength += 1

    if any(char.islower() for char in password) and any(
        char.isupper() for char in password
    ):
        strength += 1

    special_chars = "!@#$%^&*()_-+=<>?"
    if any(char in special_chars for char in password):
        strength += 1

    if strength <= 2:
        return "Weak"
    elif strength <= 4:
        return "Medium"
    else:
        return "Strong"
