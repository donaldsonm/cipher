import sys
from cs50 import get_string

# Prompt the user to correctly type in only 2 arguments
if len(sys.argv) != 2:
    sys.exit("Usage: python vigenere.py <key>")

key = sys.argv[1].upper()

# Check if the key that the user has given has only alphabetical characters in it
if not key.isalpha():
    sys.exit("Key must contain only alphabet characters")

# Prompt user for plain text to be ciphered
plain = get_string("plaintext: ")
print("ciphertext: ", end="")

# Counter is to be used to wrap back around to beginning of key if length of plaintext is greater than key
counter = 0

# For loop that changes characters of plain text for the length of plainttext
for i in range(len(plain)):

    ascii = ord(plain[i])

    # If the character is an alphabet character, add the key value to it and print cipher
    if plain[i].isalpha():
        cipher = (ord(key[counter % len(key)]) - 65) + ascii

        # Wrap back around to A when reaching Z in both uppercase and lowercase plain text characters
        if ascii >= 65 and ascii <= 90:
            while cipher > 90:
                cipher -= 26
        if ascii >= 97 and ascii <= 122:
            while cipher > 122:
                cipher -= 26

        print(f"{chr(cipher)}", end="")
        counter += 1

    # If not an alphabet character, leave it alone
    else:
        print(f"{plain[i]}", end="")
print()