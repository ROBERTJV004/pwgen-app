import random
import string

def check_strength(password):
    if len(password) < 6:
        return "Weak"
    elif len(password) < 10:
        return "Medium"
    else:
        return "Strong"


def generate_password(length, include_numbers, include_symbols):
    password = ""
    chars = string.ascii_letters
    if include_numbers:
        chars += string.digits
    if include_symbols:
        chars += string.punctuation
    for i in range(length):
        password += random.choice(chars)
    return password

print("Welcome to Password Generator!")
print("-" * 30)

while True:
    try:
        length = int(input("\nHow long should the password be? "))
        if length <= 0:
            print("Length must be greater than 0!")
            continue
    except ValueError:
        print("Please enter a valid number!")
        continue
    
    include_numbers = input("Include numbers? (yes/no): ").lower() == "yes"
    include_symbols = input("Include symbols? (yes/no): ").lower() == "yes"
    
    password = generate_password(length, include_numbers, include_symbols)
    print("Password:", password)
    print("Strength:", check_strength(password))
    
    save = input("Save to file? (yes/no): ").lower()
    if save == "yes":
        with open("passwords.txt", "a") as f:
            f.write(f"{password}\n")
        print("Password saved to passwords.txt!")
    
    again = input("\nGenerate another? (yes/no): ").lower()
    if again != "yes":
        print("Thanks for using Password Generator!")
        break
