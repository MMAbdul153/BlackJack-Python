from random import randint

def print_card_name(card_rank):
    if card_rank == 1:
        card_name = 'Ace'
    elif card_rank == 11:
        card_name = 'Jack'
    elif card_rank == 12:
        card_name = 'Queen'
    elif card_rank == 13:
        card_name = 'King'
    else:
        card_name = card_rank

    if card_rank == 8 or card_rank == 1:
        print('Drew an ' + str(card_name))
    elif card_rank < 1 or card_rank > 13:
        print('BAD CARD')
    else:
        print('Drew a ' + str(card_name))

def draw_card():
    card_rank = randint(1, 13)
    print_card_name(card_rank)

    if card_rank == 11 or card_rank == 12 or card_rank == 13:
        card_value = 10
    elif card_rank == 1:
        card_value = 11
    else:
        card_value = card_rank

    return card_value

def print_header(message):
    print('-----------')
    print(message)
    print('-----------')

def draw_starting_hand(name):
    print_header(name.upper() + ' TURN')
    return draw_card() + draw_card()

def print_end_turn_status(hand_value):
    print('Final hand: ' + str(hand_value) + '.')

    if hand_value == 21:
        print('BLACKJACK!')
    elif hand_value > 21:
        print('BUST.')

def get_end_game_status(player_hand, dealer_hand):
    if player_hand <= 21 and (player_hand > dealer_hand or dealer_hand > 21):
        return "win"
    elif player_hand > 21 or (dealer_hand <= 21 and dealer_hand > player_hand):
        return "lose"
    else:
        return "push"

def get_player_hand(player_hand):
    should_hit = 'y'
    while player_hand < 21:
        should_hit = input("You have {}. Hit (y/n)? ".format(player_hand))
        if should_hit == 'n':
            break
        elif should_hit != 'y':
            print("Sorry I didn't get that.")
        else:
            player_hand = player_hand + draw_card()
    print_end_turn_status(player_hand)
    return player_hand

def get_dealer_hand():
    dealer_hand = draw_starting_hand("DEALER")
    while dealer_hand < 17:
        print("Dealer has {}.".format(dealer_hand))
        dealer_hand = dealer_hand + draw_card()
    print_end_turn_status(dealer_hand)
    return dealer_hand

def check_elimination(player, score_board, player_board):
    index = player_board.index(player)
    if score_board[index] <= 0:
        return player  # Return the player to be eliminated

# Start the game
player_board = []
score_board = []
player_hand_table = []
num_players = int(input("Welcome to Blackjack! How many players? "))
i = 1
while i <= num_players:
    player = input(f"What is player {i}'s name? ")
    player_board.append(player)
    score_board.append(3)
    i += 1

while score_board:
    # Players' turns
    player_hand_table = []
    for player in player_board:
        player_hand = draw_starting_hand(f"{player}'S")
        player_hand = get_player_hand(player_hand)
        player_hand_table.append(player_hand)

    d_hand = get_dealer_hand()
    print_header('GAME RESULT')

    # Evaluate results and update scores
    eliminations = []
    for player in player_board:
        index = player_board.index(player)
        p_hand = player_hand_table[index]
        result = get_end_game_status(p_hand, d_hand)
        if result == "win":
            score_board[index] += 1
            print(f"{player} wins! Score: {score_board[index]}")
        elif result == "lose":
            score_board[index] -= 1
            print(f"{player} loses! Score: {score_board[index]}")
        elif result == "push":
            print(f"{player} pushes! Score: {score_board[index]}")
        
        # Check for eliminations after the scores are updated
        check = check_elimination(player, score_board, player_board)
        if check:
            eliminations.append(check)

    # Remove eliminated players
    for eliminated_player in eliminations:
        index = player_board.index(eliminated_player)
        print(f"{eliminated_player} eliminated!")
        player_board.pop(index)
        score_board.pop(index)

    # Check if all players are eliminated
    if not player_board:
        print("All players eliminated!")
        break

    # Ask if they want to play another round
    play_hand = input("Do you want to play another hand (y/n)? ")
    if play_hand == "n":
        break
    elif play_hand != "y":
        print("Sorry, I didn't get that.")

