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

        # Capitalize the question (in case it's not capitalized) and add the question mark
        clean_split[0] = clean_split[0].capitalize()
        if not clean_split[0].endswith("?"):
            clean_split[0] += "?"
        # Lowercase the second and third entries
        clean_split[1] = clean_split[1].lower()
        clean_split[2] = clean_split[2].lower()

        table.append(clean_split)

def input_handler():
    while True:
        usr_input = input().lower()
        if usr_input == "y" or usr_input == "yes":
            return True
        elif usr_input == "n" or usr_input == "no":
            return False
        else:
            print("Answer yes or no: ", end="")

def learning(row, column):
    if input_handler():
        print("I win!")
    else:
        print("what a pitty!")

        guessed_animal = table[row][column]
        
        new_row = []
        print("What was the correct animal? ", end="")
        correct_animal = input().lower()
        
        print(f"Give yes/no question to distinguish {correct_animal} from {guessed_animal}: ", end="")
        new_row.append(input().capitalize())

        print(f"What is the answer for {correct_animal}? ", end="")
        if input_handler():
            new_row.append(correct_animal)
            new_row.append(guessed_animal)
        else:
            new_row.append(guessed_animal)
            new_row.append(correct_animal)

        write_database(row, column, new_row)

def write_database(row, column, new_row):
    table.append(new_row)
    table[row][column] = table.index(new_row)

    with open(database, "w") as f:
        index = 0
        for element in table:
            line = f"{index} -- {element[0]} -- {element[1]} -- {element[2]}\n"
            f.write(line)
            index += 1

idx = 0
while True:
    current_row = table[idx]

    print(current_row[0] + " (Yes/No) ", end="")
        
    if input_handler():
        if current_row[1].isdigit():
            idx = int(current_row[1])
        else:
            print("I think I know it!")
            print(f"Is it a {current_row[1]}?" + " (Yes/No) ", end="")
            learning(idx, 1)
            break

    else:
        if current_row[2].isdigit():
            idx = int(current_row[2])
        else:
            print("I think I know it!")
            print(f"Is it a {current_row[2]}?" + " (Yes/No) ", end="")
            learning(idx, 2)
            break
