import tkinter as tk
from random import randint
import time

# Kartendaten
symbols = ("Diamonds", "Hearts", "Clubs", "Spades")
types = ("Two", "Three", "Four", "Five", "Six", "Seven",
         "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")

worth_of_cards = {
    "Ace": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6,
    "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
    "Jack": 11, "Queen": 11, "King": 11
}

# Spiellogik
sum_of_player = 0
sum_of_dealer = 0
end = False

# GUI Setup
root = tk.Tk()
root.title("Blackjack Light")
root.geometry("400x400")

output = tk.Text(root, height=15, width=45, state="disabled", wrap="word")
output.pack(pady=10)

def show_message(msg):
    output.config(state="normal")
    output.insert("end", msg + "\n")
    output.see("end")
    output.config(state="disabled")

def draw_card():
    symbol = symbols[randint(0, 3)]
    typ = types[randint(0, 12)]
    return typ, symbol, worth_of_cards[typ]

def start_game():
    global sum_of_player, end
    sum_of_player = 0
    end = False
    output.config(state="normal")
    output.delete(1.0, "end")
    output.config(state="disabled")
    card = draw_card()
    sum_of_player += card[2]
    show_message(f"Your card is the {card[0]} of {card[1]}")
    show_message(f"Current Worth: {sum_of_player}")

def another_card():
    global sum_of_player, end
    if end: 
        return

    if sum_of_player >= 19:
        _, _, value = draw_card()
        sum_of_player += value
    else:
        card = draw_card()
        sum_of_player += card[2]
        show_message(f"Your new card is the {card[0]} of {card[1]}")
        show_message(f"Current Worth: {sum_of_player}")

    if sum_of_player > 21:
        show_message("Too High! Game Over!")
        end = True
    elif sum_of_player == 21:
        show_message("Perfect! You Won!")
        end = True

def stop_game():
    global end, sum_of_player, sum_of_dealer
    if end:
        return
    end = True
    show_message(f"Your final Count is: {sum_of_player}")
    dealer_cards_amount = randint(2, 4)
    sum_of_dealer = 0
    show_message("Dealer draws:")

    for _ in range(dealer_cards_amount):
        card = draw_card()
        sum_of_dealer += card[2]
        show_message(f"{card[0]} of {card[1]}   (Worth: {sum_of_dealer})")
        if sum_of_dealer > 21:
            show_message("Dealer got too high!\nCongratulations! You Won!")
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
