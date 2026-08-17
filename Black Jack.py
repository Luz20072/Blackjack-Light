from random import *
import time


symbols = ("Diamonds", "Hearts", "Clubs", "Spades")

type = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")

worth_of_cards = {
    "Ace" : 1,
    "Two" : 2,
    "Three" : 3,
    "Four" : 4,
    "Five" : 5,
    "Six" : 6,
    "Seven" : 7,
    "Eight" : 8,
    "Nine" : 9,
    "Ten" : 10,
    "Jack" : 11,
    "Queen" : 11,
    "King" : 11
}
sum_of_player = 0
end = False

symbol_number01 = randint(0, 3)
type_number01 = randint(0, 12)

sum_of_player = worth_of_cards[type[type_number01]]

print("Your Card is the " + type[type_number01] + " of " + symbols[symbol_number01])
print(f"Current Worth ", sum_of_player)

while end != True:
    yn = input("Another Card? (yes/no): ").lower()

    if yn == "yes":
        if sum_of_player >= 19:
            greed_protection = randint(2, 11)
            sum_of_player = sum_of_player + worth_of_cards[type[greed_protection]]
        elif sum_of_player < 19:
            symbol_number_extra = randint(0, 3)
            type_number_extra = randint(0, 12)
            sum_of_player = sum_of_player + worth_of_cards[type[type_number_extra]]
            print("Your new card is the " + type[type_number_extra] + " of " +  symbols[symbol_number_extra])
            print(f"Current Worth ", sum_of_player)
            if sum_of_player > 21:
                time.sleep(0.75)
                print("To High! Game Over!")
                end = True
            elif sum_of_player == 21:
                time.sleep(0.75)
                print("Perfect! You Won!")
                end = True

    if yn == "no":
        print(f"Your final Count is: ", sum_of_player)
        dealer_cards_amount = randint(2, 4)
        sum_of_dealer = 0
        print("Drawing Dealer's Cards")
        print("Dealer draws: ")
        for drawing in range(dealer_cards_amount):
            symbol_number_dealer = randint(0, 3)
            type_number_dealer = randint(0, 12)
            sum_of_dealer = sum_of_dealer + worth_of_cards[type[type_number_dealer]]
            print(type[type_number_dealer] + " of " + symbols[symbol_number_dealer], "      (Worth: ", sum_of_dealer, ")")
            if sum_of_dealer > 21:
                print("Dealer got to high!")
                print("Congratulations! You Won!")
                break
            time.sleep(0.75)

        time.sleep(0.25)
        if sum_of_dealer <= 21:
            print("Final Dealer-Worth: ", sum_of_dealer)    
           
        if sum_of_dealer <= 21:    
            if sum_of_dealer < sum_of_player:
                print(sum_of_player, " > ", sum_of_dealer)
                print("Congratulations! You Won!")
            elif sum_of_dealer == sum_of_player:
                print(sum_of_player, " = ", sum_of_dealer)
                print("Tie!")
            elif sum_of_dealer > sum_of_player:
                print(sum_of_player, " < ", sum_of_dealer)
                print("Oh No! You Lost!")

        end = True

