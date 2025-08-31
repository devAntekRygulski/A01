import random 


cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
points = {
    'A': 11,
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10
}

def play_one_round(player_hold, verbosity):
    """
    Play a single round of blackjack.
    """
    player_hand = [random.choice(cards), random.choice(cards)]
    dealer_hand = [random.choice(cards), random.choice(cards)]

    # Player's turn
    player_points = 0
    dealer_points = 0

    for card in player_hand:
        player_points += points[card]
    for cardd in dealer_hand:
        dealer_points += points[cardd]

    if verbosity == 2:
        print("\nPlayer's inital hand: ")
        for card in player_hand:
            print("[{}] ".format(card), end="")
        print("\nDealer's inital hand: ")
        for card in dealer_hand:
            print("[{}] ".format(card), end="")

    # Player's turn
    while True:
        if player_points >= player_hold:
            break
        drawn_card = random.choice(cards)
        if verbosity == 2:
            print("\nPlayer drew the card: [{}]".format(drawn_card), end="")
        player_hand.append(drawn_card)
        player_points += points[drawn_card]

    # Dealer's turn
    while True:
        if dealer_points > 16 or player_points > 21:
            break
        drawn_card = random.choice(cards)
        if verbosity == 2:
            print("\nDealer drew the card: [{}]".format(drawn_card), end="")
        dealer_hand.append(drawn_card)
        dealer_points += points[drawn_card]

    # Determine winner

    return_value = ""

    if player_points > 21:
        return_value = "loss"
    elif dealer_points > 21 or player_points > dealer_points:
        return_value = "win"
    elif player_points == dealer_points:
        return_value = "push"
    else:
        return_value = "loss"

    if verbosity == 0:
        return return_value
    if verbosity == 1:
        print("Player has: ")
        for card in player_hand:
            print("[{}] ".format(card), end="")
        print("\nDealer has: ")
        for card in dealer_hand:
            print("[{}] ".format(card), end="")
        if return_value == "win":
            print("\nOutcome = Win - player was better")
        elif return_value == "loss":
            print("\nOutcome = Loss - dealer was better")
        elif return_value == "push":
            print("\nOutcome = Push - both at {}".format(player_points))
        return return_value

def simulate(rounds=100, verbosity=0):
    """
    Simulate multiple rounds of blackjack.
    """
    hold_values = [14, 15, 16, 17, 18, 19, 20, 21]
    results = {}

    for hold in hold_values:
        wins = 0
        loss = 0
        push = 0
        for _ in range(rounds):
            result = play_one_round(hold, verbosity)
            if result == "win":
                wins += 1
            elif result == "loss":
                loss += 1
            elif result == "push":
                push += 1
        results[hold] = [wins/rounds, push/rounds, loss/rounds]

    print()
    return results

print(simulate(10000, 0))