import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Join it with the animals database filename
database = os.path.join(script_dir, "animals.dat")

table = []

with open(database, "r") as f:
    for line in f:
        if line.strip() == "":  # Avoid processing extra empty lines
            break

        raw_split = line.split("--")

        raw_split.pop(0)  # Remove the unnecessary question index (first column in the table)
        # Note for self: .pop() actually returns the removed value, so theoretically del is more efficient, but it's negligible here

        clean_split = []
        for item in raw_split:
            clean_split.append(item.strip())

        clean_split[0] += "?"  # Add the missing question mark to the question

        table.append(clean_split)

print(table)
