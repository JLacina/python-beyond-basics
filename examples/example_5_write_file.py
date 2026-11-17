"""
Write lines of text to a file, three different ways.

Mode "w" creates the file or OVERWRITES it. Use "a" to append instead.
All three versions produce the same data/output.txt.
"""
lines = [
    "I have eaten",
    "the plums",
    "that were in",
    "the icebox",
]

# Simplest
with open("data/output.txt", "w", encoding="utf-8") as file:
    for line in lines:
        file.write(line + "\n")

# With .join()
with open("data/output.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(lines))

# With a generator expression
with open("data/output.txt", "w", encoding="utf-8") as file:
    # .writelines doesn't add \n
    file.writelines(line + "\n" for line in lines)
