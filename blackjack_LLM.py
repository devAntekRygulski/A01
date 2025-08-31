# blackjack_cs362.py
import random

RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
# CS362 mapping: A always 11; face cards 10; numeric as value
VALUE_MAP = {
    'A': 11,
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10
}

def draw_card():
    """Return a rank sampled with replacement."""
    return random.choice(RANKS)

def hand_value(hand):
    """Sum card values. For CS362 Ace is always 11."""
    return sum(VALUE_MAP[c] for c in hand)

def fmt_hand(hand):
    """Format a hand like [J][3][A]"""
    return "".join(f"[{c}]" for c in hand)

def play_one_round(player_hold, verbosity=0):
    """
    Play a single round for a given player_hold threshold.
    Returns 'win', 'push', or 'loss' from player's perspective.
    Also prints per verbosity mode.
    """
    # Initial deal alternately: player, dealer, player, dealer
    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]

    if verbosity >= 2:
        print("Initial hands:")
        print("Player has:", fmt_hand(player_hand), "=>", hand_value(player_hand))
        print("Dealer has:", fmt_hand(dealer_hand), "=>", hand_value(dealer_hand))

    # Player's turn: hit while total < player_hold
    while True:
        p_total = hand_value(player_hand)
        if p_total >= player_hold or p_total > 21:
            break
        # Hit
        card = draw_card()
        player_hand.append(card)
        if verbosity >= 2:
            print("Player hits:", f"[{card}]", "=>", fmt_hand(player_hand), hand_value(player_hand))

    p_total = hand_value(player_hand)
    player_busted = p_total > 21

    # Dealer's turn: dealer hits while dealer total <=16 AND player has not busted
    if not player_busted:
        while True:
            d_total = hand_value(dealer_hand)
            if d_total >= 17:
                break
            # dealer must hit if <= 16
            card = draw_card()
            dealer_hand.append(card)
            if verbosity >= 2:
                print("Dealer hits:", f"[{card}]", "=>", fmt_hand(dealer_hand), hand_value(dealer_hand))
    else:
        # If player busted, dealer may still have cards but per rules dealer only hits if player hasn't busted.
        if verbosity >= 2:
            print("Player busted; dealer does not hit further per rules.")

    d_total = hand_value(dealer_hand)
    dealer_busted = d_total > 21

    # Determine outcome as per CS362 conventions:
    # - If player busted => Loss (assignment explicitly asks to treat this as loss even if dealer also busts).
    # - Else if dealer busted => Win
    # - Else compare totals: player>dealer => Win, equal => Push, else Loss
    if player_busted:
        outcome = 'loss'
        reason = "Player busted"
    elif dealer_busted:
        outcome = 'win'
        reason = "Dealer busted"
    else:
        if p_total > d_total:
            outcome = 'win'
            reason = f"Player {p_total} > Dealer {d_total}"
        elif p_total == d_total:
            outcome = 'push'
            reason = f"Both at {p_total}"
        else:
            outcome = 'loss'
            reason = f"Dealer {d_total} > Player {p_total}"

    if verbosity >= 1:
        print("Player has:", fmt_hand(player_hand), "=>", p_total)
        print("Dealer has:", fmt_hand(dealer_hand), "=>", d_total)
        print("Outcome =", outcome.capitalize(), "-", reason)
        print()

    return outcome

def simulate(rounds=100, verbosity=0):
    """
    Run simulations for hold values 14 through 21 inclusive.
    Returns a dict mapping hold_value -> [win_frac, push_frac, loss_frac]
    Verbosity:
      0 - no output
      1 - print final hands & outcome per round
      2 - print initial hands and each card received during the round
    """
    results = {}
    hold_values = list(range(14, 22))  # 14..21 inclusive

    for hold in hold_values:
        wins = pushes = losses = 0
        for _ in range(rounds):
            outcome = play_one_round(hold, verbosity=verbosity)
            if outcome == 'win':
                wins += 1
            elif outcome == 'push':
                pushes += 1
            elif outcome == 'loss':
                losses += 1
        # fractions as real numbers
        results[hold] = [wins / rounds, pushes / rounds, losses / rounds]

    return results

if __name__ == "__main__":
    # Example run: 10_000 rounds per hold value (be aware this will take time)
    import argparse
    parser = argparse.ArgumentParser(description="Blackjack CS362 simulator")
    parser.add_argument("--rounds", type=int, default=10000, help="rounds per hold value")
    parser.add_argument("--verbosity", type=int, choices=[0,1,2], default=0)
    args = parser.parse_args()

    res = simulate(rounds=args.rounds, verbosity=args.verbosity)
    # Print nicely
    for hold in sorted(res.keys()):
        w, p, l = res[hold]
        print(f"{hold}: Win={w:.6f}, Push={p:.6f}, Loss={l:.6f}")
