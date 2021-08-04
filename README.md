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

## To simulate and visualize an existing game from a pgn file
```python viewgame.py pgn_files\nabaty_fridman_2018.pgn 2 english```

- 1st argument must be a path to a pgn file
- 2nd argument is the time (in seconds) between each move during the simulation
- 3rd argument is the language used in the pgn file ("english" or "french" supported)
