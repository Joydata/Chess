This is a personnal project to implement chess game with Python

# Quick run
```
git clone https://github.com/Joydata/Chess.git
cd Chess
pip3 install -r requirements.txt
```
## To Play a game vs the computer
```python playgame.py api``` if you want the computer to beat you (no offense !)

```python playgame.py random``` if you want the computer to play random moves

Chess moves must be written in english algebraic format. For example 'e4' or 'Nf3' if you play whites.

## To simulate and visualize an existing game from a pgn file
```python viewgame.py pgn_files\nabaty_fridman_2018.pgn 2 english```

- 1st argument must be a path to a pgn file
- 2nd argument is the time (in seconds) between each move during the simulation
- 3rd argument is the language used in the pgn file ("english" or "french" supported)

# More information about the project

## Content
- Chesspiece.py : Implements a Chesspiece class.
- Square.py : Implements a Square class.
- Chessboard.py : Implements a Chessboard class.
- Chessgame.py : Implements a Chessgame class.
- playgame.py : Implements and calls a function to play chess against an algorithm.
- viewgame.py : Calls Chessgame class methods to launch the visualisation of a chess game contained in a pgn file.
- requirements.txt : Contains the python libraries needed for the project
- pgn_files folder : Contains a few pgn files that can be used as examples

## Remarks
- The code implements all the moves of chess (including castling or "prise-en-passant")
- The code implements the mating rules and the draw by stalemate rule
- The board visualization is done using simple ASCII method

## Next steps
- Improve the board visualization (ASCII Diagram methods or better).
- Implement additional draw rules : threefold repetition rule, 50-move rule, dead position.
- Implement resigning and draw by mutual agreement.
- Implement the possibility to save the moves in a pgn when playing against the algorithm.
- Implement the half-move clock counter.
