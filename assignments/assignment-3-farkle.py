WINNING_SCORE = 2000  # winning score
cur_player = 0  # index of the current player
winner = ''  # name of the winner

print("Let's play farkle!")

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
    player_confirmation = input("is this correct? Yes/No ").lower()
    if  player_confirmation == "n" or player_confirmation == "no":
        players = player_names(num_players)
    elif player_confirmation == "y" or player_confirmation == "yes":
        break
    else:
        print("Answer yes/no (y/n)!")

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

    for dice in throw:
        count[dice] += 1

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

# print(calc_score([1, 2, 3, 4, 5, 6]))  # Testing
