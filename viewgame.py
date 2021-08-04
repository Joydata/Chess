from Chessgame import *
import sys

if __name__ == "__main__":
    game_file = sys.argv[1]
    wait_time = int(sys.argv[2])
    is_french = False
    
    if len(sys.argv) > 3:
        if sys.argv[3] == 'fr':
            is_french = True            
    
    game = Chessgame(game_file, french = is_french)
    game.playgame(timer = wait_time)