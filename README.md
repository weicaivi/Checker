# Checker

# Setup

Running the code in this repository requires using a number of
Python libraries. We recommend creating a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
before installing these libraries. To do so, run the
following from the root of your local repository:

    python3 -m venv venv

To activate your virtual environment, run the following:

    source venv/bin/activate

To install the required Python libraries run the following:

    pip3 install -r requirements.txt

To deactivate the virtual environment (e.g., because you're done
working on the `connectm` code), just run the following:

## TUI

Two players can play against each other in the terminal, by running the following:

```
    python3 src/tui.py
```

The TUI then displays a board in the terminal. The player in red starts first, by inputing the coordinate of the piece they want to move and where they want to move it to. Then player in black makes their move. At each step, the terminal gives user hints on what are the pieces that can be moved and where are the possible destinations they want to move the selected piece to. All inputs should be in the format of a tuple.

## GUI

To run the GUI, run the following from the root of the repository:

```
    python3 src/gui.py
```

The GUI displays the state of the board. In the game, the player holding the red piece move first. To select a piece, simply click on the piece. If the piece can be moved, all the movable square would become blue. Click on one of the blue square to move the piece. For the case of multiple steps of jumps, the program would show the possible first jump destination, then showing the following destinations. Notice the checker game used the touch-move rule, once you select a piece, you must move that piece if you can. When the game ends, the program would show the result in the cmd

GUI supports checker game with different sizes, to change the size, run

```
    python3 src/gui.py --size
```

GUI supports size from 6 to 20

## BOT

There are two bot classes:

- `RandomBot`: A bot that only moves at random
- `SmartBot`: implements a strategy to maximize its chance of winning.
  - It will adopt the following strategy:
    - Take the move that will travel the longest distance. Usually this means the SmartBot will jump whenever possible and only moves if there's no way to jump
    - If the moves have the same distance, pick a random one

_A Note on ties:_

- Total move_count made by both bots is tracked during each game. When move_count is greater than 250, this is usually the edge case where both players have only one piece left and it is usually the king of each player. It cound end up in an infinite loop of game where neither king could kill the other and ends up only moving back and forth. In this scenario, we end the game and count this as a tie

`bots.py` is default to running 10,000 simulated games between a RandomBot and a SmartBot, and the percentage of wins and ties will be printed.
You can control the number of simulated games using the `-n <number of games>` parameter to `bots.py`. You can also change the type of players using the `--player1 <type of player 1>` and `--player2 <type of player 2>` parameters.

For example:

```
cd src
python3 bot.py --player1 random --player2 random -n 100
Bot 1 (random) wins: 41.00%
Bot 2 (random) wins: 59.00%
Ties: 0.00%

python3 bot.py -n 100
Bot 1 (random) wins: 27.00%
Bot 2 (smart) wins: 56.00%
Ties: 17.00%
```
