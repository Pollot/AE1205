WINNING_SCORE = 2000 # winning score
cur_player = 0 # index of the current player
winner = '' # name of the winner

print("Let's play farkle!")

while True:
    try:
        num_players = int(input("Enter the number of players: "))
        break
    except ValueError:
        print("The number of players needs to be an integer!")

scores = [0] * num_players

def player_names(num_players):
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
