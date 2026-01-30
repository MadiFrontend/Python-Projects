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
