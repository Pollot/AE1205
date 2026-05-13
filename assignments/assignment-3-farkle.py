from random import randint

WINNING_SCORE = 2000

print("Let's play farkle!\n")

while True:
    try:
        num_players = int(input("Enter the number of players: "))
        break
    except ValueError:
        print("The number of players needs to be an integer!")

scores = [0] * num_players

def player_names(num_players: int) -> list:
    players = []

    print("Enter a name for each player.")
    for i in range(num_players):
        players.append(input(f"Enter the name for player {i+1}: ").capitalize())  # i+1, because i starts at 0

    print("The chosen players are:")
    for player in players:
        print(player, end=", ")

    return players

players = player_names(num_players)

while True:
    player_confirmation = input("is this correct? (Yes/No) ").lower()
    if  player_confirmation == "n" or player_confirmation == "no":
        players = player_names(num_players)
    elif player_confirmation == "y" or player_confirmation == "yes":
        break
    else:
        print("Answer Yes/No (y/n)!")

def calc_score(throw: list[int]) -> int:
    score = 0

    if sorted(throw) == [1, 2, 3, 4, 5, 6]:
        score = 2500
        return score
    
    count = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }

    for face in throw:
        count[face] += 1

    for face in range(1, 7):
        if face == 1:
            base_score = 1000
        else:
            base_score = face * 100

        if count[face] == 6:
            score += base_score * 4
        elif count[face] == 5:
            score += base_score * 3
        elif count[face] == 4:
            score += base_score * 2
        elif count[face] == 3:
            score += base_score
        elif face == 1:
            score += count[face] * 100
        elif face == 5:
            score += count[face] * 50

    return score

def dice_roll(num_dice: int) -> list:
    result = []

    for _ in range(num_dice):
        result.append(randint(1, 6))

    return result

def is_valid_selection(throw: list[int]) -> bool:
    if sorted(throw) == [1, 2, 3, 4, 5, 6]:
        return True

    count = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }

    for face in throw:
        count[face] += 1

    for face in [2, 3, 4, 6]:
        if count[face] == 1 or count[face] == 2:
            return False  # Only score points in groups of more than 2

    return True

cur_player = 0  # Index of the current player
winner = ""  # Name of the winner

while not winner:
    round_score = 0
    num_dice = 6
    print(f"\nIt's your turn {players[cur_player]}!")
    while True:
        roll = dice_roll(num_dice)
        print("\nYour rolls:")
        for i in range(len(roll)):
            print(f"{i+1}: {roll[i]}")  # i+1, because i starts at 0

        if calc_score(roll) == 0:
            print("Farkle!")
            input("Press enter to continue ")
            break
        else:
            while True:
                raw_selected_dice = input("\nWhich dice do you want to keep (separate them with commas)? ").split(",")
                clean_selected_dice = []
                try:
                    for element in raw_selected_dice:
                        clean_selected_dice.append(int(element))
                except ValueError:
                    print("Input integer numbers separated with commas!")
                    continue
                
                out_of_index = False
                for element in clean_selected_dice:
                    if not 1 <= element <= len(roll):
                        out_of_index = True
                if out_of_index:
                    print("Choose dice from the available rolls!")
                    continue
                
                if len(clean_selected_dice) != len(set(clean_selected_dice)):
                    print("You cannot select the same die twice!")
                    continue

                kept_dice = []
                for die in clean_selected_dice:
                    kept_dice.append(roll[die-1])  # -1, because selected indexes are +1
                
                if calc_score(kept_dice) == 0:
                    print("You must select dice that score points!")
                    continue
                
                if not is_valid_selection(kept_dice):
                    print("All selected dice must be scoring!")
                    continue

                break

            round_score += calc_score(kept_dice)
            num_dice -= len(kept_dice)

            print(f"\nCurrent score: {round_score}")
            print(f"Remaining dice: {num_dice}")

            if num_dice == 0:
                print("Hot dice!")
                print("You get all dice back!")
                num_dice = 6

            while True:
                player_choice = input("\nDo you want to bank your score and end the round? (Yes/No) ").lower()
                if  player_choice == "n" or player_choice == "no":
                    end_round = False
                    break
                elif player_choice == "y" or player_choice == "yes":
                    end_round = True
                    break
                else:
                    print("Answer yes/no (y/n)!")

            if end_round:
                scores[cur_player] += round_score
                if scores[cur_player] >= WINNING_SCORE:
                    winner = players[cur_player]
                break

    if cur_player < num_players-1:
        cur_player += 1
    else:
        print("\nTotal scores after the round:")
        for i, player in enumerate(players):
            print(f"{player}: {scores[i]}")
        cur_player = 0

print(f"\nThe winner is: {winner}! Gambling rocks!")
