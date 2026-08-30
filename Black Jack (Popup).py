```python
import tkinter as tk
from random import shuffle


# =========================================================
# Card Data
# =========================================================

SUITS = (
    "Diamonds",
    "Hearts",
    "Clubs",
    "Spades"
)

CARD_TYPES = (
    "Two", "Three", "Four", "Five", "Six", "Seven",
    "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"
)

CARD_VALUES = {
    "Ace": 11,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10
}

deck = []


# =========================================================
# Statistics
# =========================================================

games_played = 0
wins = 0
losses = 0
ties = 0
blackjack_wins = 0

total_winnings = 0
total_losses = 0

biggest_win = 0
biggest_loss = 0


# =========================================================
# Betting System
# =========================================================

balance = 1000
current_bet = 0


# =========================================================
# Hands
# =========================================================

player_hand = []
dealer_hand = []

game_over = False


# =========================================================
# Game Logic
# =========================================================

def create_deck():
    """Create and shuffle a standard 52-card deck."""
    global deck

    deck = []

    for suit in SUITS:
        for card_type in CARD_TYPES:
            deck.append(
                (card_type, suit, CARD_VALUES[card_type])
            )

    shuffle(deck)


def calculate_hand_value(hand):
    """
    Calculate the value of a hand.

    Aces initially count as 11. If the hand exceeds 21,
    aces are changed to a value of 1 where necessary.
    """
    value = sum(card[2] for card in hand)

    aces = sum(
        1 for card in hand
        if card[0] == "Ace"
    )

    while value > 21 and aces > 0:
        value -= 10
        aces -= 1

    return value


def is_blackjack(hand):
    """Return True if the hand is a natural blackjack."""
    return (
        len(hand) == 2
        and calculate_hand_value(hand) == 21
    )


def draw_card():
    """Draw and return one card from the deck."""
    if not deck:
        return None

    return deck.pop()


# =========================================================
# Statistics and Betting
# =========================================================

def record_game(result, blackjack=False):
    """Update statistics and balance after a completed game."""
    global games_played
    global wins, losses, ties, blackjack_wins
    global balance, current_bet
    global total_winnings, total_losses
    global biggest_win, biggest_loss

    games_played += 1

    if result == "win":
        wins += 1

        if blackjack:
            blackjack_wins += 1

            profit = current_bet * 1.5
            balance += current_bet * 2.5

        else:
            profit = current_bet
            balance += current_bet * 2

        total_winnings += profit

        if profit > biggest_win:
            biggest_win = profit

    elif result == "loss":
        losses += 1

        loss = current_bet

        total_losses += loss

        if loss > biggest_loss:
            biggest_loss = loss

    elif result == "tie":
        ties += 1

        balance += current_bet

    current_bet = 0


def place_bet(amount):
    """Place a bet if the amount is valid and affordable."""
    global balance, current_bet

    if amount <= 0:
        return False

    if amount > balance:
        return False

    current_bet = amount
    balance -= amount

    return True


# =========================================================
# GUI
# =========================================================

root = tk.Tk()
root.title("Blackjack Light")
root.geometry("500x400")


output = tk.Text(
    root,
    height=15,
    width=55,
    state="disabled",
    wrap="word"
)

output.pack(pady=10)


def show_message(message):
    """Display a message in the game output."""
    output.config(state="normal")

    output.insert(
        "end",
        message + "\n"
    )

    output.see("end")
    output.config(state="disabled")


def update_buttons(game_running):
    """Enable or disable buttons depending on the game state."""
    if game_running:
        btn_start.config(state="disabled")
        btn_hit.config(state="normal")
        btn_stand.config(state="normal")
        btn_statistics.config(state="disabled")

    else:
        btn_start.config(state="normal")
        btn_hit.config(state="disabled")
        btn_stand.config(state="disabled")
        btn_statistics.config(state="normal")


def end_game():
    """End the current game and reset both hands."""
    global game_over
    global player_hand, dealer_hand

    game_over = True

    update_buttons(False)

    player_hand = []
    dealer_hand = []


# =========================================================
# Statistics Window
# =========================================================

def show_statistics():
    """Open a window displaying the current game statistics."""
    statistics_window = tk.Toplevel(root)

    statistics_window.title("Statistics")
    statistics_window.geometry("320x400")
    statistics_window.resizable(False, False)

    tk.Label(
        statistics_window,
        text="Statistics",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    if games_played == 0:
        tk.Label(
            statistics_window,
            text="No games played yet!"
        ).pack(pady=20)

        return

    win_rate = wins / games_played * 100
    loss_rate = losses / games_played * 100
    tie_rate = ties / games_played * 100
    blackjack_rate = (
        blackjack_wins / games_played * 100
    )

    statistics_text = (
        f"Balance: {balance}\n\n"

        f"Games played: {games_played}\n"
        f"Wins: {wins}\n"
        f"Losses: {losses}\n"
        f"Ties: {ties}\n"
        f"Blackjack wins: {blackjack_wins}\n\n"

        f"Win rate: {win_rate:.1f}%\n"
        f"Loss rate: {loss_rate:.1f}%\n"
        f"Tie rate: {tie_rate:.1f}%\n"
        f"Blackjack rate: {blackjack_rate:.1f}%\n\n"

        f"Total winnings: {total_winnings}\n"
        f"Total losses: {total_losses}\n"
        f"Biggest win: {biggest_win}\n"
        f"Biggest loss: {biggest_loss}"
    )

    tk.Label(
        statistics_window,
        text=statistics_text,
        justify="left"
    ).pack()


# =========================================================
# Betting Window
# =========================================================

def bet_window():
    """Open the window used to enter a bet."""
    window = tk.Toplevel(root)

    window.title("Place Bet")
    window.geometry("300x170")
    window.resizable(False, False)

    window.transient(root)
    window.grab_set()

    tk.Label(
        window,
        text=f"Your balance: {balance}"
    ).pack(pady=(15, 5))

    tk.Label(
        window,
        text="Enter your bet:"
    ).pack()

    bet_entry = tk.Entry(window)
    bet_entry.pack(pady=5)
    bet_entry.focus()

    def confirm_bet():
        try:
            amount = int(bet_entry.get())

        except ValueError:
            show_message("Invalid bet!")
            return

        if not place_bet(amount):
            show_message(
                "Invalid bet or insufficient balance!"
            )
            return

        window.destroy()
        start_round()

    tk.Button(
        window,
        text="Place Bet",
        command=confirm_bet
    ).pack(pady=5)

    window.bind(
        "<Return>",
        lambda event: confirm_bet()
    )


# =========================================================
# Dealer Logic
# =========================================================

def dealer_draw_step():
    """
    Let the dealer draw cards until reaching at least 17.

    The dealer stands on 17, including soft 17.
    """
    global dealer_hand
    global balance, current_bet

    dealer_value = calculate_hand_value(dealer_hand)

    if dealer_value < 17:
        card = draw_card()

        if card is None:
            show_message("No cards left!")

            balance += current_bet
            current_bet = 0

            end_game()
            return

        dealer_hand.append(card)

        dealer_value = calculate_hand_value(dealer_hand)

        show_message(
            f"Dealer draws: "
            f"{card[0]} of {card[1]}"
        )

        show_message(
            f"Dealer's current hand value: "
            f"{dealer_value}"
        )

        if dealer_value > 21:
            show_message("Dealer busts!")
            show_message("You won!")

            record_game("win")
            end_game()

            return

        root.after(
            500,
            dealer_draw_step
        )

        return

    show_message(
        f"Dealer's final hand value: "
        f"{dealer_value}"
    )

    player_value = calculate_hand_value(player_hand)

    if dealer_value < player_value:
        show_message("You won!")
        record_game("win")

    elif dealer_value == player_value:
        show_message("Tie!")
        record_game("tie")

    else:
        show_message("You lost!")
        record_game("loss")

    end_game()


# =========================================================
# Game Start
# =========================================================

def start_game():
    """Start a new round by opening the betting window."""
    if balance <= 0:
        show_message("You have no money left!")
        return

    bet_window()


def start_round():
    """Start a new round after a valid bet has been placed."""
    global game_over
    global player_hand, dealer_hand
    global balance, current_bet

    player_hand = []
    dealer_hand = []

    game_over = False

    update_buttons(True)

    # Create a new deck when fewer than four cards remain.
    if len(deck) < 4:
        create_deck()

    output.config(state="normal")
    output.delete(1.0, "end")
    output.config(state="disabled")

    show_message(
        f"Current bet: {current_bet}"
    )

    show_message(
        f"Remaining balance: {balance}"
    )

    show_message("")

    # Deal two cards to the player.
    for _ in range(2):
        card = draw_card()

        if card is None:
            show_message("No cards left!")

            balance += current_bet
            current_bet = 0

            end_game()
            return

        player_hand.append(card)

        show_message(
            f"Your card: "
            f"{card[0]} of {card[1]}"
        )

    player_value = calculate_hand_value(player_hand)

    show_message(
        f"Your current hand value: "
        f"{player_value}"
    )

    # Deal two cards to the dealer.
    for _ in range(2):
        card = draw_card()

        if card is None:
            show_message("No cards left!")

            balance += current_bet
            current_bet = 0

            end_game()
            return

        dealer_hand.append(card)

    # Check for blackjack.
    player_blackjack = is_blackjack(player_hand)
    dealer_blackjack = is_blackjack(dealer_hand)

    # Both have blackjack.
    if player_blackjack and dealer_blackjack:
        show_message("Dealer's cards:")

        show_message(
            f"{dealer_hand[0][0]} "
            f"of {dealer_hand[0][1]}"
        )

        show_message(
            f"{dealer_hand[1][0]} "
            f"of {dealer_hand[1][1]}"
        )

        show_message(
            "Both have Blackjack! It's a tie!"
        )

        record_game("tie")
        end_game()

        return

    # Player has blackjack.
    if player_blackjack:
        show_message(
            "You have Blackjack! You won!"
        )

        record_game(
            "win",
            blackjack=True
        )

        end_game()

        return

    # Dealer has blackjack.
    if dealer_blackjack:
        show_message("Dealer's cards:")

        show_message(
            f"{dealer_hand[0][0]} "
            f"of {dealer_hand[0][1]}"
        )

        show_message(
            f"{dealer_hand[1][0]} "
            f"of {dealer_hand[1][1]}"
        )

        show_message(
            "Dealer has Blackjack! You lost!"
        )

        record_game("loss")
        end_game()

        return

    # No blackjack.
    show_message("Dealer's cards:")

    show_message(
        f"{dealer_hand[0][0]} "
        f"of {dealer_hand[0][1]}"
    )

    show_message("Hidden card: ?")


# =========================================================
# Player Actions
# =========================================================

def hit():
    """Draw another card for the player."""
    global game_over
    global player_hand
    global balance, current_bet

    if game_over:
        return

    card = draw_card()

    if card is None:
        show_message("No cards left!")

        balance += current_bet
        current_bet = 0

        end_game()
        return

    player_hand.append(card)

    player_value = calculate_hand_value(player_hand)

    show_message(
        f"Your new card: "
        f"{card[0]} of {card[1]}"
    )

    show_message(
        f"Your current hand value: "
        f"{player_value}"
    )

    if player_value > 21:
        show_message("You bust! Game over!")

        record_game("loss")
        end_game()

    elif player_value == 21:
        show_message("21! You won!")

        record_game("win")
        end_game()


def stand():
    """Stop drawing cards and let the dealer play."""
    global game_over

    if game_over:
        return

    game_over = True

    player_value = calculate_hand_value(player_hand)

    show_message(
        f"Your final hand value: "
        f"{player_value}"
    )

    if len(dealer_hand) >= 2:
        show_message(
            "Dealer reveals the hidden card:"
        )

        show_message(
            f"{dealer_hand[1][0]} "
            f"of {dealer_hand[1][1]}"
        )

    dealer_value = calculate_hand_value(dealer_hand)

    show_message(
        f"Dealer's current hand value: "
        f"{dealer_value}"
    )

    dealer_draw_step()


# =========================================================
# Buttons
# =========================================================

button_frame = tk.Frame(root)
button_frame.pack(pady=10)


btn_start = tk.Button(
    button_frame,
    text="Start Game",
    command=start_game
)

btn_start.grid(
    row=0,
    column=0,
    padx=5
)


btn_hit = tk.Button(
    button_frame,
    text="Hit",
    command=hit
)

btn_hit.grid(
    row=0,
    column=1,
    padx=5
)


btn_stand = tk.Button(
    button_frame,
    text="Stand",
    command=stand
)

btn_stand.grid(
    row=0,
    column=2,
    padx=5
)


btn_statistics = tk.Button(
    button_frame,
    text="Statistics",
    command=show_statistics
)

btn_statistics.grid(
    row=0,
    column=3,
    padx=5
)


# =========================================================
# Application Start
# =========================================================

create_deck()
update_buttons(False)

root.mainloop()
```
