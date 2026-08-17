from random import *
import time


symbols = ("Karo", "Herz", "Kreuz", "Pik")

type = ("Zwei", "Drei", "Vier", "Fuenf", "Sechs", "Sieben", "Acht", "Neun", "Zehn", "Bube", "Dame", "Koenig", "Ass")

worth_of_cards = {
    "Ass" : 1,
    "Zwei" : 2,
    "Drei" : 3,
    "Vier" : 4,
    "Fuenf" : 5,
    "Sechs" : 6,
    "Sieben" : 7,
    "Acht" : 8,
    "Neun" : 9,
    "Zehn" : 10,
    "Bube" : 11,
    "Dame" : 11,
    "Koenig" : 11
}
sum_of_player = 0
end = False

symbol_number01 = randint(0, 3)
type_number01 = randint(0, 12)

sum_of_player = worth_of_cards[type[type_number01]]

print("Deine erste Karte ist die " + symbols[symbol_number01] + " " + type[type_number01])
print(f"Aktuelle Summe: ", sum_of_player)

while end != True:
    yn = input("Noch eine Karte ziehen? (ja/nein): ").lower()

    if yn == "ja":
        if sum_of_player >= 19:
            greed_protection = randint(2, 11)
            sum_of_player = sum_of_player + worth_of_cards[type[greed_protection]]
        elif sum_of_player < 19:
            symbol_number_extra = randint(0, 3)
            type_number_extra = randint(0, 12)
            sum_of_player = sum_of_player + worth_of_cards[type[type_number_extra]]
            print("Deine neue Karte ist: " + symbols[symbol_number_extra] + " " +  type[type_number_extra])
            print(f"Aktuelle Summe: ", sum_of_player)
            if sum_of_player > 21:
                time.sleep(0.75)
                print("Zu Viel! Du hast verloren!")
                end = True
            elif sum_of_player == 21:
                time.sleep(0.75)
                print("Blackjack! Du hast gewonnen!")
                end = True

    if yn == "nein":
        print(f"Deine Endsumme ist: ", sum_of_player)
        dealer_cards_amount = randint(2, 4)
        sum_of_dealer = 0
        print("Der Dealer zieht:")
        for drawing in range(dealer_cards_amount):
            symbol_number_dealer = randint(0, 3)
            type_number_dealer = randint(0, 12)
            sum_of_dealer = sum_of_dealer + worth_of_cards[type[type_number_dealer]]
            print(symbols[symbol_number_dealer] + " " + type[type_number_dealer], "      (Atueller Wert: ", sum_of_dealer, ")")
            if sum_of_dealer > 21:
                print("Der Dealer hat zu viel gezogen!")
                print("Glückwunsch! Du hast gewonnen!")
                break
            time.sleep(0.75)

        time.sleep(0.25)
        if sum_of_dealer <= 21:
            print("Endsumme des Dealers: ", sum_of_dealer)    
           
        if sum_of_dealer <= 21:    
            if sum_of_dealer < sum_of_player:
                print(sum_of_player, " > ", sum_of_dealer)
                print("Glückwunsch! Du hast gewonnen!")
            elif sum_of_dealer == sum_of_player:
                print(sum_of_player, " = ", sum_of_dealer)
                print("Unentschieden!")
            elif sum_of_dealer > sum_of_player:
                print(sum_of_player, " < ", sum_of_dealer)
                print("Oh Nein! Du hast verloren!")

        end = True

