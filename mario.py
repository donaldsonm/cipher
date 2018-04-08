from cs50 import get_int

# Make sure the user gives me an integer height between 0 and 23
while True:
    height = get_int("Integer: ")
    if height >= 0 and height <= 23:
        break

# For each row, print a certain number of spaces and hashes
for rows in range(height):
    for space1 in range(height - (rows + 1)):
        print(" ", end="")
    for hash1 in range(rows + 1):
        print("#", end="")
    for space2 in range(2):
        print(" ", end="")
    for hash2 in range(rows + 1):
        print("#", end="")
    print()
