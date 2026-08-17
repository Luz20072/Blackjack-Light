import tkinter as tk
from random import shuffle
import time

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


# Spiellogik

def create_deck():
    global deck

    deck = []

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


sum_of_player = 0
sum_of_dealer = 0
end = False

# GUI Setup
root = tk.Tk()
root.title("Blackjack Light")
root.geometry("400x400")

output = tk.Text(root, height=15, width=45, state="disabled", wrap="word")
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

    return deck.pop()

def start_game():
    global sum_of_player, sum_of_dealer, end, player_hand, dealer_hand

    player_blackjack = False
    dealer_blackjack = False

    sum_of_player = 0
    sum_of_dealer = 0

    player_hand = []
    dealer_hand = []

    end = False

    create_deck()

    output.config(state="normal")
    output.delete(1.0, "end")
    output.config(state="disabled")

    # Spieler zieht zwei Karten
    for _ in range(2):
        card = draw_card()
        player_hand.append(card)
        show_message(f"Your card is the {card[0]} of {card[1]}")

    sum_of_player = calculate_hand_value(player_hand)

    show_message(f"Current Worth: {sum_of_player}")

    # Dealer zieht zwei Karten
    for _ in range(2):
        card = draw_card()
        dealer_hand.append(card)

    sum_of_dealer = calculate_hand_value(dealer_hand)

    # Blackjack prüfen
    if is_blackjack(player_hand):
        player_blackjack = True

    if is_blackjack(dealer_hand):
        dealer_blackjack = True

    # Blackjack-Ergebnisse
    if player_blackjack and dealer_blackjack:
        show_message("Dealer's cards:")
        show_message(f"{dealer_hand[0][0]} of {dealer_hand[0][1]}")
        show_message(f"{dealer_hand[1][0]} of {dealer_hand[1][1]}")
        show_message("Both have Blackjack! It's a Tie!")
        end = True
        return

    elif player_blackjack:
        show_message("You've got Blackjack! You won!")
        end = True
        return

    elif dealer_blackjack:
        show_message("Dealer's cards:")
        show_message(f"{dealer_hand[0][0]} of {dealer_hand[0][1]}")
        show_message(f"{dealer_hand[1][0]} of {dealer_hand[1][1]}")
        show_message("Dealer has Blackjack! You lost!")
        end = True
        return

    # Kein Blackjack
    show_message("Dealer's cards:")
    show_message(f"{dealer_hand[0][0]} of {dealer_hand[0][1]}")
    show_message("Hidden card: ?")

def another_card():
    global sum_of_player, end, player_hand

    if end:
        return

    card = draw_card()

    if card is None:
        show_message("No cards left!")
        end = True
        return

    player_hand.append(card)

    sum_of_player = calculate_hand_value(player_hand)

    show_message(f"Your new card is the {card[0]} of {card[1]}")
    show_message(f"Current Worth: {sum_of_player}")

    if sum_of_player > 21:
        show_message("Too High! Game Over!")
        end = True
    elif sum_of_player == 21:
        show_message("Perfect! You Won!")
        end = True

def stop_game():
    global end, sum_of_player, sum_of_dealer, dealer_hand

    if end:
        return

    end = True

    show_message(f"Your final Count is: {sum_of_player}")

    # Verdeckte Dealerkarte aufdecken
    show_message("Dealer reveals the hidden card:")
    show_message(f"{dealer_hand[1][0]} of {dealer_hand[1][1]}")

    sum_of_dealer = calculate_hand_value(dealer_hand)
    show_message(f"Dealer's current Worth: {sum_of_dealer}")

    # Dealer zieht bis mindestens 17
    while sum_of_dealer < 17:
        card = draw_card()

        if card is None:
            show_message("No cards left!")
            return

        dealer_hand.append(card)
        sum_of_dealer = calculate_hand_value(dealer_hand)

        show_message(f"Dealer draws: {card[0]} of {card[1]}")
        show_message(f"Dealer's current Worth: {sum_of_dealer}")

        if sum_of_dealer > 21:
            show_message("Dealer got too high!")
            show_message("Congratulations! You Won!")
            return

        root.update()
        time.sleep(0.5)

    show_message(f"Final Dealer-Worth: {sum_of_dealer}")

    if sum_of_dealer < sum_of_player:
        show_message("Congratulations! You Won!")
    elif sum_of_dealer == sum_of_player:
        show_message("Tie!")
    else:
        show_message("Oh No! You Lost!")

# Buttons
frame = tk.Frame(root)
frame.pack(pady=10)

btn_start = tk.Button(frame, text="Start Game", command=start_game)
btn_start.grid(row=0, column=0, padx=5)

btn_yes = tk.Button(frame, text="Another Card", command=another_card)
btn_yes.grid(row=0, column=1, padx=5)

btn_no = tk.Button(frame, text="Stop", command=stop_game)
btn_no.grid(row=0, column=2, padx=5)

root.mainloop()
