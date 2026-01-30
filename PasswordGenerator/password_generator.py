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


def save_password_to_file(service, username, password, filename="passwords.txt"):
    """
    Save generated password to a text file
    """
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"Service: {service}\n")
            file.write(f"Username: {username}\n")
            file.write(f"Password: {password}\n")
            file.write(f"Strength: {calculate_password_strength(password)}\n")
            file.write("-" * 40 + "\n")
        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False


def main():
    """
    Main program function with CLI interface
    """
    parser = argparse.ArgumentParser(
        description="Secure Password Generator - Python CLI Tool"
    )

    parser.add_argument(
        "-l", "--length", type=int, default=12, help="Password length (default: 12)"
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=1,
        help="Number of passwords to generate (default: 1)",
    )
    parser.add_argument(
        "-s", "--no-special", action="store_false", help="Exclude special characters"
    )
    parser.add_argument(
        "-d", "--no-digits", action="store_false", help="Exclude digits"
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Save passwords to specified file"
    )

    args = parser.parse_args()

    print("\n" + "=" * 50)
    print("      Secure Password Generator - Python")
    print("=" * 50)

    service = input("Service/Website (optional): ").strip()
    username = input("Username (optional): ").strip()

    print(f"\nPassword Generation Settings:")
    print(f"  Password length: {args.length}")
    print(f"  Number of passwords: {args.number}")
    print(f"  Use digits: {'Yes' if args.no_digits else 'No'}")
    print(f"  Use special chars: {'Yes' if args.no_special else 'No'}")
    print("-" * 40)

    passwords = []
    for i in range(args.number):
        password = generate_password(
            length=args.length,
            use_digits=args.no_digits,
            use_special_chars=args.no_special,
        )
        passwords.append(password)

        print(f"\nPassword #{i+1}:")
        print(f"  {password}")
        print(f"  Length: {len(password)} characters")
        print(f"  Strength: {calculate_password_strength(password)}")

    print("\n" + "-" * 40)

    if args.output or (service and username):
        filename = args.output if args.output else "passwords.txt"

        save_all = input(f"\nSave passwords to '{filename}'? (y/n): ").lower()

        if save_all == "y":
            success_count = 0
            for i, password in enumerate(passwords):
                service_name = (
                    f"{service}_{i+1}" if service and args.number > 1 else service
                )
                if save_password_to_file(service_name, username, password, filename):
                    success_count += 1

            if success_count > 0:
                print(f"\n{success_count} password(s) saved to '{filename}'.")

    print("\nCLI Usage Examples:")
    print("  python password_generator.py -l 16")
    print("  python password_generator.py -n 5")
    print("  python password_generator.py -s -d")
    print("  python password_generator.py -o my_passwords.txt")

    print("\n" + "=" * 50)
    print("Thank you for using Password Generator!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
