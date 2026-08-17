import tkinter as tk
from random import shuffle

# Kartendaten
symbols = ("Diamonds", "Hearts", "Clubs", "Spades")
types = ("Two", "Three", "Four", "Five", "Six", "Seven",
         "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")

worth_of_cards = {
    "Ace": 11, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6,
    "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
    "Jack": 10, "Queen": 10, "King": 10
}

deck = []
used_cards = []

# Statistik
games_played = 0
wins = 0
losses = 0
ties = 0
blackjack_wins = 0


# Spiellogik

def create_deck():
    global deck, used_cards

    deck = []
    used_cards = []

    for symbol in symbols:
        for typ in types:
            deck.append((typ, symbol, worth_of_cards[typ]))

    shuffle(deck)


def calculate_hand_value(hand):
    value = sum(card[2] for card in hand)
    aces = sum(1 for card in hand if card[0] == "Ace")

    while value > 21 and aces > 0:
        value -= 10
        aces -= 1

    return value


player_hand = []
dealer_hand = []

end = False


# GUI Setup
root = tk.Tk()
root.title("Blackjack Light")
root.geometry("500x400")

output = tk.Text(root, height=15, width=55, state="disabled", wrap="word")
output.pack(pady=10)


def is_blackjack(hand):
    return len(hand) == 2 and calculate_hand_value(hand) == 21


def show_message(msg):
    output.config(state="normal")
    output.insert("end", msg + "\n")
    output.see("end")
    output.config(state="disabled")


def draw_card():
    if not deck:
        return None

    card = deck.pop()
    used_cards.append(card)

    return card


def record_game(result, blackjack=False):
    global games_played, wins, losses, ties, blackjack_wins

    games_played += 1

    if result == "win":
        wins += 1

        if blackjack:
            blackjack_wins += 1

    elif result == "loss":
        losses += 1

    elif result == "tie":
        ties += 1


def show_statistics():
    statistics_window = tk.Toplevel(root)
    statistics_window.title("Statistics")
    statistics_window.geometry("300x300")
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
    blackjack_rate = blackjack_wins / games_played * 100

    statistics_text = (
        f"Games played: {games_played}\n"
        f"Wins: {wins}\n"
        f"Losses: {losses}\n"
        f"Ties: {ties}\n"
        f"Blackjack wins: {blackjack_wins}\n\n"
        f"Win rate: {win_rate:.1f}%\n"
        f"Loss rate: {loss_rate:.1f}%\n"
        f"Tie rate: {tie_rate:.1f}%\n"
        f"Blackjack rate: {blackjack_rate:.1f}%"
    )

    tk.Label(
        statistics_window,
        text=statistics_text,
        justify="left"
    ).pack()


def end_game():
    global end, player_hand, dealer_hand

    end = True
    update_buttons(False)

    player_hand = []
    dealer_hand = []


def dealer_draw_step():
    global dealer_hand

    dealer_value = calculate_hand_value(dealer_hand)

    if dealer_value < 17:
        card = draw_card()

        if card is None:
            show_message("No cards left!")
            end_game()
            return

        dealer_hand.append(card)
        dealer_value = calculate_hand_value(dealer_hand)

        show_message(f"Dealer draws: {card[0]} of {card[1]}")
        show_message(f"Dealer's current Worth: {dealer_value}")

        if dealer_value > 21:
            show_message("Dealer got too high!")
            show_message("Congratulations! You Won!")

            record_game("win")

            end_game()
            return

        root.after(500, dealer_draw_step)
        return

    show_message(f"Final Dealer-Worth: {dealer_value}")

    player_value = calculate_hand_value(player_hand)

    if dealer_value < player_value:
        show_message("Congratulations! You Won!")
        record_game("win")

    elif dealer_value == player_value:
        show_message("Tie!")
        record_game("tie")

    else:
        show_message("Oh No! You Lost!")
        record_game("loss")

    end_game()


def update_buttons(game_running):
    if game_running:
        btn_start.config(state="disabled")
        btn_yes.config(state="normal")
        btn_no.config(state="normal")
        btn_statistics.config(state="disabled")
    else:
        btn_start.config(state="normal")
        btn_yes.config(state="disabled")
        btn_no.config(state="disabled")
        btn_statistics.config(state="normal")


def start_game():
    global end, player_hand, dealer_hand

    player_hand = []
    dealer_hand = []

    end = False
    update_buttons(True)

    if len(deck) < 4:
        create_deck()

    output.config(state="normal")
    output.delete(1.0, "end")
    output.config(state="disabled")

    # Spieler zieht zwei Karten
    for _ in range(2):
        card = draw_card()

        if card is None:
            show_message("No cards left!")
            end_game()
            return

        player_hand.append(card)
        show_message(f"Your card is the {card[0]} of {card[1]}")

    player_value = calculate_hand_value(player_hand)

    show_message(f"Current Worth: {player_value}")

    # Dealer zieht zwei Karten
    for _ in range(2):
        card = draw_card()

        if card is None:
            show_message("No cards left!")
            end_game()
            return

        dealer_hand.append(card)

    # Blackjack prüfen
    player_blackjack = is_blackjack(player_hand)
    dealer_blackjack = is_blackjack(dealer_hand)

    # Blackjack-Ergebnisse
    if player_blackjack and dealer_blackjack:
        show_message("Dealer's cards:")
        show_message(f"{dealer_hand[0][0]} of {dealer_hand[0][1]}")
        show_message(f"{dealer_hand[1][0]} of {dealer_hand[1][1]}")
        show_message("Both have Blackjack! It's a Tie!")

        record_game("tie")

        end_game()
        return

    elif player_blackjack:
        show_message("You've got Blackjack! You won!")

        record_game("win", blackjack=True)

        end_game()
        return

    elif dealer_blackjack:
        show_message("Dealer's cards:")
        show_message(f"{dealer_hand[0][0]} of {dealer_hand[0][1]}")
        show_message(f"{dealer_hand[1][0]} of {dealer_hand[1][1]}")
        show_message("Dealer has Blackjack! You lost!")

        record_game("loss")

        end_game()
        return

    # Kein Blackjack
    show_message("Dealer's cards:")
    show_message(f"{dealer_hand[0][0]} of {dealer_hand[0][1]}")
    show_message("Hidden card: ?")


def another_card():
    global end, player_hand

    if end:
        return

    card = draw_card()

    if card is None:
        show_message("No cards left!")
        end_game()
        return

    player_hand.append(card)

    player_value = calculate_hand_value(player_hand)

    show_message(f"Your new card is the {card[0]} of {card[1]}")
    show_message(f"Current Worth: {player_value}")

    if player_value > 21:
        show_message("Too High! Game Over!")

        record_game("loss")

        end_game()

    elif player_value == 21:
        show_message("Perfect! You Won!")

        record_game("win")

        end_game()


def stop_game():
    global end

    if end:
        return

    end = True

    player_value = calculate_hand_value(player_hand)

    show_message(f"Your final Count is: {player_value}")

    # Verdeckte Dealerkarte aufdecken
    if len(dealer_hand) >= 2:
        show_message("Dealer reveals the hidden card:")
        show_message(f"{dealer_hand[1][0]} of {dealer_hand[1][1]}")

    dealer_value = calculate_hand_value(dealer_hand)
    show_message(f"Dealer's current Worth: {dealer_value}")

    dealer_draw_step()


# Buttons
frame = tk.Frame(root)
frame.pack(pady=10)

btn_start = tk.Button(frame, text="Start Game", command=start_game)
btn_start.grid(row=0, column=0, padx=5)

btn_yes = tk.Button(frame, text="Another Card", command=another_card)
btn_yes.grid(row=0, column=1, padx=5)

btn_no = tk.Button(frame, text="Stop", command=stop_game)
btn_no.grid(row=0, column=2, padx=5)

btn_statistics = tk.Button(
    frame,
    text="Statistics",
    command=show_statistics
)
btn_statistics.grid(row=0, column=3, padx=5)

update_buttons(False)

root.mainloop()