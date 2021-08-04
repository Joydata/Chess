from Chessboard import *
import time

class Chessgame():
    """
    A class to represent a Chess game.

    ...

    Attributes
    ----------
    result : str
        The final result of the game (in [1-0,0-1,1/2,1/2])
    moves : list of str
        The list of the move references of the game

    Methods
    -------
    read_moves(self, game, french=False):
        Converts the algebraic notation of a chess game (as a string) in a list of moves and store the list
        in the moves attribute of the Chessgame object. 
        The method can be used with french or english notations.
    read_pgn(self,file):
        Reads a pgn file, feeds the Chessgame object result attribute with the result of the game,
        and returns the moves of the game as a string.
    playgame(self,timer=3):
        Simulate the execution of the game on a Chessboard object, prints each move reference and the visualisation
        of the board after each move.
    """

    def __init__(self, file = None, french = False):
        if file != None:
            self.read_moves(self.read_pgn(file), french=french)
        else:
            self.result = None
            self.moves = None

    def read_moves(self, game, french = False):
        """
        Converts the algebraic notation of a chess game (as a string) in a list of moves and store the list
        in the moves attribute of the Chessgame object. 
        The method can be used with french or english notations.

        Parameters
        ----------
            game : str
                The string containing the algebraic notations of a chess game.
            french : bool
                To be set to True if the game is in french notations.
                Default is False.
        """
        result = [] # Initializing the result list
        ref_list = game.split()         
        
        for i in range(len(ref_list)):
            ref_list[i] = ref_list[i].lstrip('.-/0123456789') # Removing the move numbers
            if ref_list[i] != '':
                result.append(ref_list[i])
        
        if french:
            for index in range(len(result)):
                transTable = result[index].maketrans('TFCDR', 'RBNQK')
                result[index] = result[index].translate(transTable)
       
        self.moves = result
            
     
    def read_pgn(self, file):
        """
        Reads a pgn file, feeds the Chessgame object result attributes with the result of the game,
        and returns the moves of the game as a string.

        Parameters
        ----------
            file : str
                The path to the pgn file.
        """
        fp = open(file)
        gamestarted = False
        game = ''
        for line in fp: #Loop over the lines of the file
            if line.startswith('[Result '): 
                self.result = line[9:-3] # Result line always has this format : [Result "1-0"]
            if line.startswith('1.'): # "1."" indicates the first move of the game
                gamestarted = True
            if gamestarted:
                game += line # If we are in the game part of the file, we add the line to the result
        return game
               
    def playgame(self, timer = 3):
        """
        Simulate the execution of the Chessgame instance on a Chessboard object, prints each move reference and the visualisation
        of the board after each move.

        Parameters
        ----------
            timer : int
                The time in seconds between the execution of each move.
        """

        board = Chessboard() # Instanciating the Chessboard object
        for move in self.moves: # Loop over the moves of the Chessgame
            print(move)
            board.move(move)
            print(board)
            time.sleep(timer)  
        print(self.result) # Finishing the execution by printing the result.





