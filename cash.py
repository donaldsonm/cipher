from cs50 import get_float

# Make sure that user gives me a positive float
while True:
    change = get_float("Change owed: ")
    if change > 0:
        break

# Multiply float by 100 to prevent rounding errors
change *= 100

coincount = 0

# Use a series of while loops to identify the minimum coins required to give back their change
while change >= 25:
    change -= 25
    coincount += 1

while change >= 10:
    change -= 10
    coincount += 1

while change >= 5:
    change -= 5
    coincount += 1

while change >= 1:
    change -= 1
    coincount += 1

# Return end result
print(f"{coincount}")