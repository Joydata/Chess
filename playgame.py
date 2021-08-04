from Chessboard import *
import sys
import random
import requests

def get_move_from_api(fen):
    """
    Returns the best move calculated by Stockfish algorithm for a given configuration of the chessboard.
    The Forsyth–Edwards Notation (FEN) of the current state of the chessboard must be passed as aurgument.
    For more information on FEN : https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation

    Parameters
    ----------
        fen : str
            The Forsyth–Edwards Notation (FEN) of the current state of the chessboard.

    """
    api_url = 'https://chess.apurn.com/nextmove' 
    response = requests.post(api_url, fen) # Stockfish API call
    move = response.content.decode()  # Getting the move from API response
    return move

def game(algo = 'random'):
    """
    Launches a chess game between a player and the computer.
    Player can choose his color and enter his moves in the console.
    The function supports algebraic notation and long algebraic notation for the moves.
    The computer can play as random or using Stockfish algorithm, via an api.
    To end the game even if it is not finished, player can input 'end' in the console.


    Parameters
    ----------
        algo : str
            The algorithm used by the computer to make its moves. Can be 'random' or 'api'.
            If set to 'api', the Stockfish algorithm is used, via an api.
            Default is 'random'

    """
    api_url = 'https://chess.apurn.com/nextmove' 
    board = Chessboard()
    play = True

    # Player inputs his color on the console
    color = input('What color do you want to play ? (White or Black)')
    
    # Computer color
    other_color = (color == 'White') * 'Black' + (color == 'Black') * 'White'
    
    # If computer's color is white, it needs to play the 1st move
    if other_color == 'White':
        moves = board.possible_moves('White') # Calculating all the possible moves
        if algo == 'random':
            picked_move = random.choice(moves) # Picking a random move
        if algo == 'api':
            fen = board.encode_fen() # fen of the chessboard is needed for the API call
            try:
                picked_move = get_move_from_api(fen)  # Picking the move from API response
            except:
                picked_move = random.choice(moves)
                print("Api call didn't work, Random move picked")       
        
        print(picked_move)
        if len(picked_move) == 4 and picked_move[:2] in board.squares.keys(): # Case of a long algebraic notation
            board.smove(picked_move[:2], picked_move[2:]) # Executing the move with a long algebraic notation
        else:
            board.cmove(picked_move) # Executing the move with an algebraic notation
        print(board)

    while play: # Loop until a checkmate or a pat or the players inputs 'end' in the console
        player_move = input('What is your move ? ("end" to finish the game)')
        if player_move == 'end':
            play = False
        else:
            board.move(player_move)

            if board.is_mating(color) or board.is_pating(color): # Checking if the game is finished
                play = False
            
            if board.turn == other_color and play: # If a move was executed and game is not finished, it is now computer's turn.
                moves = board.possible_moves(board.turn) # Calculating all the possible moves
                                
                if algo=='random':
                    picked_move=random.choice(moves) # Picking a random move
                
                if algo == 'api':
                    fen = board.encode_fen() # fen of the chessboard is needed for the API call
                    try:
                        picked_move = get_move_from_api(fen)  # Picking the move from API response
                        # Converting API notation in case of castling
                        if (picked_move == 'e8g8' or picked_move == 'e1g1') and board.squares[picked_move[:2]].piece.piece_type == 'K':
                            picked_move = 'O-O'
                        elif (picked_move == 'e8c8' or picked_move == 'e1c1') and board.squares[picked_move[:2]].piece.piece_type == 'K':
                            picked_move = 'O-O-O'
                    except:
                        picked_move = random.choice(moves)
                        print("Api call didn't work, Random move picked")
                        
                print(picked_move)
                if len(picked_move) == 4 and picked_move[:2] in board.squares.keys(): # Case of a long algebraic notation
                    board.smove(picked_move[:2],picked_move[2:]) # Executing the move with a long algebraic notation
                else:
                    board.cmove(picked_move) # Executing the move with an algebraic notation
                if board.is_mating(other_color) or board.is_pating(other_color): # Checking if the game is finished
                    play = False

                    
                print(board)


if __name__ == "__main__":
    game_type = sys.argv[1]
    game(algo = game_type)
