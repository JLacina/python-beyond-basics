"""
Read a file with a number on each line. Print the sum of those numbers.

`with open(...)` closes the file automatically, even if an error happens.
If a line isn't a whole number, int() raises a ValueError.
"""
sum_ = 0  # Trailing underscore avoids shadowing the built-in sum() function
with open("data/input.txt", encoding="utf-8") as file:
    for line in file.readlines():  # Read each line (includes the "\n", which int() ignores)
        sum_ += int(line)

    file.seek(0)  # Move cursor back to the beginning
    contents = file.read()  # Return the whole file as a string
    print(contents)

print(f"The sum is {sum_}")
