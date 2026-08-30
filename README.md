# Blackjack Light

A simple Blackjack game written in Python using Tkinter.

The game provides a basic Blackjack experience with a virtual balance, betting system, statistics, and standard player and dealer actions.

## Features

* Standard 52-card deck
* Player and dealer hands
* Hit and Stand actions
* Blackjack detection
* Automatic Ace value adjustment
* Dealer draws until reaching at least 17
* Virtual betting system
* Starting balance of 1000
* Blackjack payout of 3:2
* Win, loss, and tie tracking
* Win and loss statistics
* Biggest win and loss tracking
* Separate statistics window
* No external Python libraries required

## Rules

The game follows basic Blackjack rules:

* The goal is to get as close to 21 as possible without exceeding it.
* Number cards are worth their displayed value.
* Jack, Queen, and King are worth 10.
* An Ace is worth 11 unless this would cause the hand to exceed 21, in which case it is counted as 1.
* A natural Blackjack consists of an Ace and a 10-value card.
* A regular win pays 1:1.
* A Blackjack pays 3:2.
* A tie returns the original bet.
* The dealer must draw while their hand value is below 17.
* The dealer stands on 17, including soft 17.

## Virtual Balance

The game uses a virtual balance for its betting system.

The player starts with:

```text
1000
```

No real money is involved. The balance exists only as part of the game mechanics.

## How to Run

Make sure Python is installed on your system.

Run the program with:

```bash
python blackjack.py
```

The game uses Python's built-in `tkinter` module, so no additional packages are required.

## Controls

| Button         | Function                                   |
| -------------- | ------------------------------------------ |
| **Start Game** | Start a new round and place a bet          |
| **Hit**        | Draw another card                          |
| **Stand**      | Stop drawing cards and let the dealer play |
| **Statistics** | Display game statistics                    |

## Statistics

The game tracks statistics for the current session, including:

* Games played
* Wins
* Losses
* Ties
* Blackjack wins
* Win rate
* Loss rate
* Tie rate
* Blackjack rate
* Total winnings
* Total losses
* Biggest win
* Biggest loss
* Current balance

Statistics are stored only while the application is running and are reset when the program is restarted.

## Project Structure

```text
Blackjack-Light/
├── blackjack.py
├── README.md
├── LICENSE
└── .gitignore
```

### `blackjack.py`

Contains the complete game logic and graphical user interface.

### `README.md`

Contains the project documentation and usage instructions.

### `LICENSE`

Contains the license terms for using, modifying, and distributing the project.

## Technologies

* Python
* Tkinter
* Python `random` module

No external dependencies are required.

## License

This project is licensed under the **PolyForm Noncommercial License 1.0.0**.

You are free to use, modify, and redistribute the project for permitted non-commercial purposes.

**Commercial use is not permitted.**

For the complete license terms, see the [`LICENSE`](LICENSE) file included in this repository.
