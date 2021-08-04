from Chesspiece import *
from Square import *
import copy

class Chessboard:
    """
    A class to represent a Chessboard with its pieces and its rules.

    ...

    Attributes
    ----------
    squares : dict of str: Square object
        Dictionnary containing all the square references of the chessboard as keys and the 
        associated Square objects as values.
    count : int
        The move number at the current state of the Chessboard.
    turn : str
        The next player turn to play ('White' or 'Black').
    big_castle_white : bool
        Eequals to True until the white player does a move that prevents to do a big-castling 
        in the future.
    big_castle_black : bool
        Equals to True until the black player does a move that prevents to do a big-castling 
        in the future.
    small_castle_white : bool
        Equals to True until the white player does a move that prevents to do a small-castling 
        in the future.
    small_castle_black : bool
        Equals to True until the black player does a move that prevents to do a small-castling 
        in the future.
    previous : str
        The reference of the last move played.


    Methods
    -------
    smove(self, origin, destination, promote = None, quiet = False):
        Moves a piece based on its origin and destination squares, if permitted by the rules.

    cmove(self, ref, promote = None, quiet = False):
        Moves a piece based on its reference in algebraic notation, if permitted by the rules.
    
    move(self, *args, promote = None, quiet = False):
        Operates a series of moves based on its references in algebraic notation, if permitted by the rules.

    cheat_move(self, origin, destination):
        Moves a piece based on its origin and destination squares, even if the move is not permitted by the rules.

    get_coord(self, ref):
        Returns the coordinates of a square in a tuple based on its reference.

    get_ref(self, row, line):
        Returns the reference of a square based on its coordinates.
    
    is_valid_castle(self, big = False):
        Returns a boolean indicating if a castling is possible for the current player,
        based on the state of the chessboard and the castling history.
    
    castle(self, big = False):
        Operates a castling for the current player, if permitted.

    search_piece(self, color, piece):
        Returns a list of the Chessboard square references containing a given piece with a given color.

    get_piece(self, row, line):
        returns the piece_type of the piece on given square coordinates.

    is_valid(self, origin, destination, quiet = False, turn = True):
        Returns a boolean indicating if a move is valid according to chess rules.
        Takes into account all kind of moves except castling.

    attacks(self, square):
        Returns a dictionnary which keys are all the square references attacked by the chess piece on a given square

    all_attacks(self, color = None):
        Returns a dictionnary which keys are all the square references attacked by the chess pieces of a given player,
        or of both players.

    possible_moves(self, color):
        Returns a list of the possible moves for a given player.

    is_checking(self, color):
        Returns a boolean indicating if a given player is currently checking the other one.

    is_mating(self, color):
        Returns a boolean indicating if a given player is currently mating the other one.

    is_pating(self, color):
        Returns a boolean indicating if a given player is currently pating the other one.

    encode_fen(self):
        Returns the Forsyth–Edwards Notation (FEN) of the current Chessboard position.

    """

    rows = [None,*'abcdefgh']
    lines = [None,*range(1,9)]
    
    def __init__(self):
        """
        Instantiate a Chessboard object with all attributes set to the initial values of a standard game.
        """
        #Initialisation of the attributes
        self.turn = 'White'
        self.count = 1
        self.squares = {}
        self.big_castle_white = True
        self.big_castle_black = True
        self.small_castle_white = True
        self.small_castle_black = True
        self.previous = None

        #Instantiation of the pieces
        piece_order = ['R','N','B','Q','K','B','N','R']
        line1 = [None] + [Chesspiece(type,'White') for type in piece_order]
        line2 = [None] + [Chesspiece('P','White') for i in range(8)]
        line7 = [None] + [Chesspiece('P','Black') for i in range(8)]
        line8 = [None] + [Chesspiece(type,'Black') for type in piece_order] 

        for row in range(1,9): #loop over the rows of the chessboard
            sq1 = Square(Chessboard.rows[row]+'1',line1[row]) #Instantiation of the square on line 1
            self.squares[Chessboard.rows[row]+'1'] = sq1 #Storing the square in the squares attribute of the chessboard

            sq2 = Square(Chessboard.rows[row]+'2',line2[row]) #Instantiation of the square on line 2
            self.squares[Chessboard.rows[row]+'2'] = sq2 #Storing the square in the squares attribute of the chessboard

            sq7 = Square(Chessboard.rows[row]+'7',line7[row]) #Instantiation of the square on line 7
            self.squares[Chessboard.rows[row]+'7'] = sq7 #Storing the square in the squares attribute of the chessboard

            sq8 = Square(Chessboard.rows[row]+'8',line8[row]) #Instantiation of the square on line 8
            self.squares[Chessboard.rows[row]+'8'] = sq8 #Storing the square in the squares attribute of the chessboard

            for line in range(3,7): #Loop over the lines 3 to 6 of the chessboard
                sq = Square(Chessboard.rows[row]+str(line),None) #Instantiation of the square
                self.squares[Chessboard.rows[row]+str(line)] = sq #Storing the square in the squares attribute 
                                                                    # of the chessboard

    def __str__(self):
        """
        Called by the str() built-in function and by the print statement to compute the “informal” string representation 
        of the Chessboard object.
        Returns the ASCII representation of the chessboard.
        """

        result = []

        for line_nb in range(8,0,-1):
            line = [str(self.squares[ref].piece) for ref in [letter + str(line_nb) for letter in 'abcdefgh']]
            for i in range(8):
                if line[i]=='None':
                    line[i]=' .'
            line = '%2s'*8 % tuple(line)
            result.append(str(line_nb) + ''.join(line))
        
        result.append(' ' + '%2s'*8 %('a','b','c','d','e','f','g','h'))

        result='\n'.join(result)
        return result
        
    def smove(self,origin,destination,promote=None,quiet=False):
        """
        Moves a piece of the chessboard from an origin to a destination
        The move is done only if it is valid.

        Parameters
        ----------
            origin : str
                The reference of the origin square of the move
            destination : str
                The reference of the destination square of the move
            promote : str or None
                The chosen piece in case of pawn promotion. 
                If None, the chosen piece is asked to the player and can be typed on the keyboard.
                Default is None
            quiet : boolean
                If True, additional information are printed during the execution of the move.
                Default is False.
        """
        try:
            if self.is_valid(origin,destination):
                
                # Checking moves preventing future castling
                if self.turn == 'White' and (origin == 'a1' or origin == 'e1'):
                    self.big_castle_white = False
                if self.turn == 'White' and (origin == 'h1' or origin == 'e1'):
                    self.small_castle_white = False
                if self.turn == 'Black' and (origin == 'a8' or origin == 'e8'):
                    self.big_castle_black = False
                if self.turn == 'Black' and (origin == 'h8' or origin == 'e8'):
                    self.small_castle_black = False

                #Changing the turn         
                self.turn = (self.turn == 'White') * 'Black' + (self.turn == 'Black') * 'White'
                #Adding 1 to the count if it it now white's turn 
                self.count = self.count + 1 if self.turn == 'White' else self.count           

                #Copying and removing the piece from origin square 
                piece = copy.copy(self.squares[origin].piece)
                self.squares[origin].piece = None
                #Check and print if a piece is taken (only if quiet argument is True)
                if self.squares[destination].piece != None and not quiet:
                    print(self.squares[destination].piece.color,' ',self.squares[destination].piece.piece_type,' taken')

                #Particular case of 'prise en passant'
                if piece.piece_type == 'P' and self.squares[destination].piece == None and (destination[0] != origin[0]):
                
                    e_p = destination[0] + '4' if self.turn == 'White' else destination[0] + '5' #square reference for 'prise en passant'
                    self.squares[e_p].piece = None #Removing the piece
                    if not quiet:
                        print('Pawn on ',e_p,' taken en passant')

                #Putting the piece on destination square
                self.squares[destination].piece = piece

                #Particular case of pawn promotion
                if piece.piece_type == 'P' and (destination[1] == '1' or destination[1] == '8'):
                    if promote == None:
                        promote = input('promote to ? (Q/R/B/N)') #Ask to user if promotion argument was not passed
                    self.squares[destination].piece.piece_type = promote

                #Storing the move in 'previous' attribute of the chessboard object                       
                self.previous = origin+destination
            
            else:
                print('Forbidden move')

            # Check if there is a mat, a pat or a check
            if self.is_mating((self.turn == 'White') * 'Black' + (self.turn == 'Black') * 'White'):
                print((self.turn == 'White') * '0-1' + (self.turn=='Black') * '1-0')

            elif self.is_pating((self.turn == 'White') * 'Black' + (self.turn == 'Black') * 'White'):
                print('1/2-1/2')

            elif self.is_checking((self.turn == 'White') * 'Black' + (self.turn == 'Black') * 'White'):
                if not quiet:
                    print('Check!')
        except:
            print('command not understood')

    def cmove(self, ref, promote=None, quiet=False):
        """
        Moves a piece of the chessboard based on a move reference in algebraic form.

        Parameters
        ----------
            ref : str
                The reference of the move in algebraic form
            promote : str or None
                The chosen piece in case of pawn promotion. 
                If None, the chosen piece is asked to the player and can be typed on the keyboard.
                Default is None
            quiet : bool
                If True, additional information are printed during the execution of the move.
                Default is False.
        """
        try:
            turn = self.turn
            #Cleaning the move from not needed annotations (like '+' or '!')
            if not ref[-1] in [*'12345678',*Chesspiece.Type_list,'O']:
                self.cmove(ref[:-1], quiet = quiet)
            #Checking if the move contains a promotion information at the end
            elif ref[-1] in [*Chesspiece.Type_list]:
                self.cmove(ref[:-2], promote=ref[-1], quiet=quiet)
            #Checking if the move is a small castling
            elif ref == 'O-O':
                self.castle(big=False)
            #Checking if the move is a big castling
            elif ref == 'O-O-O':
                self.castle(big=True)
            #Checking if the move is a pawn move
            elif len(ref) == 2:
                row_dest, line_dest = self.get_coord(ref)
                line_origin = line_dest - 1 if self.turn == 'White' else line_dest + 1
                ref_origin = self.get_ref(row_dest, line_origin)
                if self.squares[ref_origin].piece != None:
                    if self.squares[ref_origin].piece.piece_type == 'P' and self.squares[ref_origin].piece.color == self.turn:
                        self.smove(ref_origin, ref, promote=promote, quiet=quiet)
                else:
                    line_origin = line_origin - 1 if self.turn == 'White' else line_origin + 1
                    ref_origin = self.get_ref(row_dest, line_origin)
                    self.smove(ref_origin, ref, promote=promote, quiet=quiet)

            elif len(ref) == 3:
                #Checking if the first letter is a piece reference
                if ref[0].isupper():
                    piece = ref[0]
                    dest = ref[1:]
                    #Gathering all the candidate origin squares containing a similar piece
                    origins = self.search_piece(self.turn, piece)
                    for origin in origins:
                        #For all candidate origin squares, checking if the move would be valid. If yes, executing the move.
                        if self.is_valid(origin, dest, quiet = True):
                            self.smove(origin, dest, promote=promote, quiet = quiet)
                            break
                    if turn == self.turn: #If True, it means no move was executed during the loop
                        print('command not understood')
                elif ref[2]=='+':
                    self.cmove(ref[0:2],promote=promote,quiet=quiet)
                else:
                    print('command not understood')

            elif len(ref)==4:
                #Length of the move reference can be 4 if:
                # - There is an annotation as last character
                # - There is a 'x' in the move to signify a piece taken
                # - There is an additional row or line reference because two similar pieces can move on the same destination 

                # Checking if there is an annotation as last character
                if ref[3] == '+':
                    self.cmove(ref[0:3], promote = promote, quiet = quiet)
                # Checking if there is an 'x' to signify a piece taken
                elif ref[1] == 'x' and ref[0].isupper(): #Not a pawn
                    self.cmove(ref[0] + ref[2:], promote = promote, quiet = quiet)
                elif ref[1] == 'x' and ref[0].islower(): # Pawn case
                    dest = ref[2:]
                    row_dest, line_dest = self.get_coord(dest)
                    line_origin = line_dest - 1 if self.turn == 'White' else line_dest + 1
                    row_origin = ref[0]
                    origin = row_origin + str(line_origin)
                    self.smove(origin, dest, promote = promote, quiet = quiet)
                # Checking if there is an additional row reference after the piece reference
                elif ref[0].isupper() and ref[1] in Chessboard.rows and ref[2:] in self.squares.keys():
                    piece = ref[0]
                    dest = ref[2:]
                    origins = self.search_piece(self.turn, piece)
                    for origin in origins:
                        if origin[0] == ref[1] and self.is_valid(origin, dest, quiet = True):
                            self.smove(origin, dest, promote = promote, quiet = quiet)
                            break
                    if turn == self.turn:
                        print('command not understood')
                # Last case : there is an additional line reference after the piece reference
                else :
                    piece = ref[0]
                    dest = ref[2:]
                    origins = self.search_piece(self.turn, piece)
                    for origin in origins:
                        if origin[1] == ref[1] and self.is_valid(origin, dest, quiet = True):
                            self.smove(origin, dest, promote = promote, quiet = quiet)
                            break
                    if turn == self.turn:
                        print('command not understood')

            elif len(ref) == 5:
                #If length of the move is 5, there is additional cleaning to do :
                i = ref.find('x') #index ot the potential 'x'
                if i != -1:
                    new_ref = ref[:i]+ref[i+1:]
                else: #no 'x' found'
                    new_ref = ref 
                j = new_ref.find('+') #index ot the potential '+'
                if j!=-1:
                    new_new_ref = new_ref[:j]+ref[j+1:]
                else: #no '+' found'
                    new_new_ref=new_ref
                self.cmove(new_new_ref, promote=promote, quiet=quiet)

            
            if turn == self.turn: #If no move was executed
                print('command not understood')
        except: #If any error during the execution
            print('command not understood')

    def move(self, *args, promote=None, quiet=False):
        """
        Executes a series of moves.

        Parameters
        ----------
            args : list of strings
                The references of the moves to execute
            promote : str or None
                The chosen piece in case of pawn promotion. 
                If None, the chosen piece is asked to the player and can be typed on the keyboard.
                Default is None
            quiet : boolean
                If True, additional information are printed during the execution of the move.
                Default is False.
        """
        for ref in args:
            self.cmove(ref, promote = promote, quiet = quiet)

    def cheat_move(self, origin, destination):
        """
        Executes a move without checking that it is allowed by the rules and without updating the attributes 
        of the chessboard object.
        Parameters
        ----------
            origin : str
                The reference of the origin square of the move
            destination : str
                The reference of the destination square of the move
        """
        piece=copy.copy(self.squares[origin].piece)
        self.squares[origin].piece=None
        self.squares[destination].piece=piece

    def get_coord(self, ref):
        """
        Returns the coordinates (row, line) of a square based on the square reference.
        Parameters
        ----------
            ref : str
                The reference of the square
        """
        row = Chessboard.rows.index(ref[0])
        line = Chessboard.lines.index(int(ref[1]))
        return (row, line)

    def get_ref(self, row, line):
        """
        Returns the reference of a square as a string, based on the square coordinates (row, line).
        Parameters
        ----------
            row : int
                The row coordinate of the square.
            line : int
                The line coordinate of the square
        """
        ref = Chessboard.rows[row] + str(Chessboard.lines[line])
        return ref    

    def is_valid_castle(self, big = False, quiet = True):
        """
        Returns a boolean indicating if a castling is valid or not, based on the current state of the chessboard.
        Parameters
        ----------
            big : bool
                True if the castling to be checked is on queen side (big-castling)
                Default = False
            quiet : bool
                If False, the reason to refuse the castling is printed in case it's applicable.
                Default is True.

        """

        turn = self.turn
        other_turn = (turn != 'White') * 'White' + (turn != 'Black') * 'Black'
        # test1 : Castling not prevented by a previous move of the king or the rook
        # test2 : No piece between the king and the rook
        # test3 : Squares on which the king will move not attacked
        if turn == 'White':
            if big:
                test1 = self.big_castle_white == True 
                test2 = (any([self.squares[ref].piece != None for ref in ['b1', 'c1', 'd1']])) == False
                test3 = (any([ref in self.all_attacks(other_turn) for ref in ['c1', 'd1', 'e1']])) == False

            else:
                test1 = self.small_castle_white == True
                test2 = (any([self.squares[ref].piece != None for ref in ['f1', 'g1']])) == False
                test3 = (any([ref in self.all_attacks(other_turn) for ref in ['e1', 'f1',' g1']])) == False

        if turn == 'Black':
            if big:
                test1 = self.big_castle_black == True
                test2 = (any([self.squares[ref].piece != None for ref in ['b8', 'c8', 'd8']])) == False
                test3 = (any([ref in self.all_attacks(other_turn) for ref in ['c8', 'd8', 'e8']])) == False

            else:
                test1 = self.small_castle_black == True
                test2 = (any([self.squares[ref].piece != None for ref in ['f8', 'g8']])) == False
                test3 = (any([ref in self.all_attacks(other_turn) for ref in ['e8', 'f8', 'g8']])) == False

        castle_type = 'big' * big + 'small' * (not big)
        if quiet == False:
            if test1 == False:
                print(f"You can't do a {castle_type} castle anymore")
            elif test2 == False:
                print(f"You can't do a {castle_type} castle as there is a piece in the way")
            elif test3 == False:
                print(f"You can't do a {castle_type} castle as you are under attack")

        return test1 and test2 and test3 #All tests must pass to allow the castling
    
    def castle(self,big=False):
        """
        Operates a castling on the chessboard, if allowed.
        Parameters
        ----------
            big : bool
                True if the castling to be done is on queen side (big-castling)
                Default = False
        """
        if self.turn == 'White':
            if big:
                if self.is_valid_castle(big = True, quiet = False):
                    self.cheat_move('a1','d1')
                    self.cheat_move('e1','c1')
                    self.turn = 'Black'
                    self.big_castle_white = False
                    self.small_castle_white = False
                    self.previous = 'O-O-O'
                    return
            else:
                if self.is_valid_castle(big = False, quiet = False):
                    self.cheat_move('h1','f1')
                    self.cheat_move('e1','g1')
                    self.turn = 'Black'
                    self.big_castle_white = False
                    self.small_castle_white = False
                    self.previous = 'O-O'
                    return

        if self.turn == 'Black':
            if big:
                if self.is_valid_castle(big = True, quiet = False):
                    self.cheat_move('a8','d8')
                    self.cheat_move('e8','c8')
                    self.turn = 'White'
                    self.count = self.count + 1
                    self.big_castle_black = False
                    self.small_castle_black = False
                    self.previous = 'O-O-O'
                    return
            else:
                if self.is_valid_castle(big = False, quiet = False):
                    self.cheat_move('h8','f8')
                    self.cheat_move('e8','g8')
                    self.turn = 'White'
                    self.count = self.count + 1
                    self.big_castle_black = False
                    self.small_castle_black = False
                    self.previous = 'O-O'
                    return             
            
    def search_piece(self,color,piece):
        """
        Returns a list with the reference(s) of all the square(s) containing a given piece with a given color.
        Parameters
        ----------
            color : string
                The color of the piece to be searched.
            piece : string
                The piece_type of the piece to be searched.

        """
        result = []
        for ref, square in self.squares.items():
            if square.piece != None:
                if square.piece.piece_type == piece and square.piece.color == color:
                    result.append(ref)

        return result
        
    def get_piece(self,row,line):
        """
        Returns the piece_type of the piece positionned on a square, based on the square coordinates.
        Parameters
        ----------
            row : int
                The row coordinate of the square to be checked.
            line : int
                The line coordinate of the square to be checked.

        """
        try :
            return self.squares[Chessboard.rows[row]+str(Chessboard.lines[line])].piece.piece_type
        except:
            return None

    def is_valid(self,origin,destination,quiet=False,turn=True):
        """
        Returns a boolean indicating if a move is permitted or not.
        Parameters
        ----------
            origin : str
                The reference of the origin square of the move to be checked.
            destination : str
                The reference of the destination square of the move to be checked.
            quiet : bool
                If True, additional information are printed during the execution.
                Default is True.
            turn : bool
                If True, the current turn of the chessboard is taken into account to check if the move is valid.
                Default is True.

        """
        # Checking if there is a piece on the origin square
        if self.squares[origin].piece == None:
            if not quiet:
                print('No piece here !')
            return False

        # If turn parameter is True, checking if the piece is of the right color to do a move
        if self.squares[origin].piece.color != self.turn and turn:
            if not quiet:
                print('Not your turn !')
            return False

        # Storing the color of the player whose it is not the turn to play
        other_turn = (self.turn == 'White') * 'Black' + (self.turn == 'Black') * 'White'
        
        # Copying the board in test_board
        test_board=copy.deepcopy(self)
        
        # Removing the piece in the particular case of "Prise en passant"
        (row_origin, line_origin) = test_board.get_coord(origin)
        (row_dest, line_dest) = test_board.get_coord(destination)
        if line_origin == 5 and line_dest == 6 and test_board.squares[origin].piece.color == 'White' and row_origin - row_dest in [-1,1]:
            if test_board.previous == destination[0] + '7' + destination[0] + '5' and test_board.squares[destination[0] + '5'].piece.piece_type == 'P':
                test_board.squares[destination[0] + '5'].piece = None
        if line_origin == 4 and line_dest == 3 and test_board.squares[origin].piece.color == 'Black' and row_origin-row_dest in [-1,1]:
            if test_board.previous == destination[0] + '2' + destination[0] + '4' and test_board.squares[destination[0] + '4'].piece.piece_type == 'P':
                test_board.squares[destination[0] + '4'].piece = None
        
        # moving the piece on the test board
        test_board.cheat_move(origin,destination)


        # Checking that after the move, the player who just moved is not checked by the opponent. If yes, the move is not permitted.
        if test_board.is_checking(other_turn):
            if not quiet:
                print("You can't do this move because you would be in check")
            return False

        # Storing the list of squares attacked by the piece at the origin square
        attacks=self.attacks(self.squares[origin])

        # Checking that the destination square is in the list of attacked squares       
        if destination in attacks.keys():
                return True

        # Checking additional particular cases for pawns that would allow the move
        if self.squares[origin].piece.piece_type == 'P':
            
            (row_origin, line_origin) = self.get_coord(origin) 
            (row_dest, line_dest) = self.get_coord(destination)

            # Particular case for white pawns first move
            if line_origin == 2 and self.squares[origin].piece.color == 'White':
                # The pawn must stay in the same row (we are not in the case of a piece taken otherwise the function already returned before)
                # It must also go forward of 1 or  2 squares
                if row_dest != row_origin or line_dest - line_origin <=0 or line_dest - line_origin > 2:
                    return False
                # The destination square must be empty
                if self.squares[destination].piece != None:
                    return False
                # If the pawn is moving to line 4, the line 3 must also be free
                if line_dest == 4 and self.squares[destination[0]+'3'].piece != None:
                    return False
                return True

            # Particular case for black pawns first move     
            if line_origin == 7 and self.squares[origin].piece.color == 'Black':
                # The pawn must stay in the same row (we are not in the case of a piece taken otherwise the function already returned before)
                # It must also go forward of 1 or  2 squares
                if row_dest != row_origin or line_origin - line_dest <=0 or line_origin - line_dest>2:
                    return False
                # The destination square must be empty
                if self.squares[destination].piece != None:
                    return False
                # If the pawn is moving to line 5, the line 6 must also be free
                if line_dest == 5 and self.squares[destination[0] + '6'].piece != None:
                    return False
                return True

            # Particular case of "Prise en passant" by a white pawn
            if line_origin == 5 and line_dest == 6 and self.squares[origin].piece.color == 'White' and row_origin - row_dest in [-1,1]:
                if self.previous == destination[0] + '7' + destination[0] + '5' and self.squares[destination[0] + '5'].piece.piece_type == 'P':
                    return True
            # Particular case of "Prise en passant" by a black pawn   
            if line_origin == 4 and line_dest == 3 and self.squares[origin].piece.color == 'Black' and row_origin-row_dest in [-1,1]:
                if self.previous == destination[0] + '2' + destination[0] + '4' and self.squares[destination[0] + '4'].piece.piece_type == 'P':
                    return True

            # Particular case of a forward move for a pawn (not taken into account before because on a forward move, a pawn
            # is moving on a square on which it cannot take a piece)
            if self.squares[origin].piece.color == 'White':
                return row_dest == row_origin and line_dest - line_origin == 1 and self.squares[destination].piece==None
            if self.squares[origin].piece.color=='Black':
                return row_dest==row_origin and line_origin-line_dest==1 and self.squares[destination].piece==None

        return False
        
    def attacks(self,square):
        """
        Returns a Dictionnary which keys are the squares references attacked by the piece on a given square.
        Parameters
        ----------
            square : Square object
                The Square object on which is placed the piece to be checked.

        """
        # Initializing the result dictionary
        result = {}

        # Storing the row and line indexes of the square to be checked
        (row_index , line_index) = self.get_coord(square.name)
        
        # Calculating the attacked squares if the piece is a pawn
        if square.piece.piece_type == 'P':
            if square.piece.color == 'White': # Case of a white pawn
                if row_index != 1 and line_index != 8: # Case of a white pawn not on the left or top edges of the board
                    attack_1 = Chessboard.rows[row_index-1] + str(Chessboard.lines[line_index+1]) # square reference at the forward left 
                                                                                                    # of the pawn
                    if self.squares[attack_1].piece != None: # A pawn only attacks in diagonal if there is a piece to take
                        result[attack_1] = None # Storing the square reference in the result dictionnary
                
                if row_index != 8 and line_index != 8: # Case of a white pawn not on the right or top edges of the board
                    attack_2=Chessboard.rows[row_index+1] + str(Chessboard.lines[line_index+1]) # square reference on the forward right
                                                                                                # of the pawn
                    if self.squares[attack_2].piece != None: # A pawn only attacks in diagonal if there is a piece to take
                        result[attack_2] = None # Storing the square reference in the result dictionnary
                
            if square.piece.color == 'Black': # Case of a black pawn
                if row_index != 1 and line_index != 1: # Case of a black pawn not on the left or bottom edges of the board
                    attack_1 = Chessboard.rows[row_index-1] + str(Chessboard.lines[line_index-1]) # square reference at the bacward left
                                                                                                # of the pawn
                    if self.squares[attack_1].piece != None: # A pawn only attacks in diagonal if there is a piece to take
                        result[attack_1] = None # Storing the square reference in the result dictionnary
                
                if row_index != 8 and line_index != 1: # Case of a black pawn not on the right or bottom edges of the board
                    attack_2 = Chessboard.rows[row_index+1] + str(Chessboard.lines[line_index-1]) # square reference at the bacward right
                                                                                                    # of the pawn
                    if self.squares[attack_2].piece != None: # A pawn only attacks in diagonal if there is a piece to take
                        result[attack_2] = None # Storing the square reference in the result dictionnary
                
        # Calculating the attacked squares if the piece is a King
        if square.piece.piece_type == 'K':
            if row_index != 1 and line_index != 1: # Excluding the case of a king on the left or bottom edges of the board
                attack_1 = Chessboard.rows[row_index-1]+str(Chessboard.lines[line_index-1]) # backward left attack
                result[attack_1] = None           
            if row_index != 1 and line_index != 8: # Excluding the case of a king on the left or top edges of the board
                attack_2 = Chessboard.rows[row_index-1] + str(Chessboard.lines[line_index+1]) # forward left attack
                result[attack_2] = None
            if line_index != 1: # Excluding the case of a king on the bottom edge of the board
                attack_3 = Chessboard.rows[row_index]+str(Chessboard.lines[line_index-1]) # backward center attack
                result[attack_3] = None  
            if row_index != 8 and line_index != 1:# Excluding the case of a king on the right or bottom edges of the board
                attack_4 = Chessboard.rows[row_index+1] + str(Chessboard.lines[line_index-1]) # backward right attack
                result[attack_4]=None
            if row_index != 8 and line_index != 8: # Excluding the case of a king on the right or top edges of the board
                attack_5 = Chessboard.rows[row_index+1] + str(Chessboard.lines[line_index+1]) # forward right attack
                result[attack_5] = None
            if line_index != 8: # Excluding the case of a king on top edges of the board
                attack_6=Chessboard.rows[row_index]+str(Chessboard.lines[line_index+1]) # forward center attack
                result[attack_6]=None
            if row_index != 1: # Excluding the case of a king on the left edge of the board
                attack_7 = Chessboard.rows[row_index-1]+str(Chessboard.lines[line_index]) # left attack
                result[attack_7] = None
            if row_index != 8: # Excluding the case of a king on the right edge of the board
                attack_8 = Chessboard.rows[row_index+1]+str(Chessboard.lines[line_index]) # right attack
                result[attack_8] = None

        # Calculating the attacked squares if the piece is a Rook
        if square.piece.piece_type=='R':

            # Attacked squares in front of the rook :
            if row_index < 8:
                row_index += 1
                
                while self.get_piece(row_index, line_index) == None and row_index < 8: # Loop over the free squares in front of the rook
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index]) 
                    result[attack] = None # Storing the square in the result
                    row_index += 1 # Going to the next square

                attack = Chessboard.rows[row_index]+str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result
                
            # Attacked squares behind the rook
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes
            if row_index > 1:
                row_index -= 1

                while self.get_piece(row_index,line_index) == None and row_index > 1: # Loop over the free squares behind the rook
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the square in the result
                    row_index-=1 # Going to the next square
                    
                attack = Chessboard.rows[row_index]+str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result

            # Attacked squares on the right of the rook
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes
            if line_index < 8:
                line_index+=1
            
                while self.get_piece(row_index,line_index) == None and line_index <8: # Loop over the free squares right of the rook
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the square in the result
                    line_index += 1 # Going to the next square
                    
                attack=Chessboard.rows[row_index]+str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result

            # Attacked squares on the left of the rook
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes
            if line_index > 1:
                line_index -= 1

                while self.get_piece(row_index,line_index) == None and line_index > 1: # Loop over the free squares right of the rook
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the square in the result
                    line_index -= 1 # Going to the next square
                    
                attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result

        # Calculating the attacked squares if the piece is a Bishop
        if square.piece.piece_type == 'B':

            # Attacked squares on the front-right of the bishop :
            if row_index < 8 and line_index<8 :
                row_index += 1
                line_index += 1
                
                while self.get_piece(row_index,line_index) == None and row_index < 8 and line_index<8 : # Loop over the free squares front-right
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the square in the result
                    row_index += 1
                    line_index += 1 # Going to the next square

                attack=Chessboard.rows[row_index]+str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result    
            
            # Attacked squares behind-right of the bishop :
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes
            if row_index > 1 and line_index<8 :
                row_index -= 1
                line_index += 1
                
                while self.get_piece(row_index,line_index) == None and row_index > 1 and line_index<8: # Loop over the free squares behind-right
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the square in the result
                    row_index -= 1
                    line_index += 1 # Going to the next square
                    
                attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result

            # Attacked squares in front-left of the bishop :
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes
            if row_index < 8 and line_index > 1:
                row_index += 1
                line_index -= 1
            
                while self.get_piece(row_index,line_index) == None and row_index < 8 and line_index > 1: # Loop over the free squares front-left
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the square in the result
                    row_index += 1
                    line_index -= 1 # Going to the next square
                    
                attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result

            # Attacked squares behind-left of the bishop :
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes
            if row_index > 1 and line_index > 1:
                row_index -= 1
                line_index -= 1

                while self.get_piece(row_index,line_index) == None and row_index > 1 and line_index > 1: # Loop over the free squares behind-left
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the square in the result
                    line_index -= 1
                    row_index -= 1 # Going to the next square
                    
                attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result
        
        # Calculating the attacked squares if the piece is a Knight
        if square.piece.piece_type == 'N':
            if row_index > 1: # Excluding knights on the left edge
                if line_index < 7: # Excluding knights on the 2 top edge lines
                    row_attack = row_index - 1
                    line_attack = line_index + 2
                    attack = Chessboard.rows[row_attack] + str(Chessboard.lines[line_attack]) # Attacked square on forward - left
                    result[attack] = None # Storing the attacked square in the result
                
                if line_index > 2: # Excluding knights on the 2 bottom edge lines
                    row_attack = row_index - 1
                    line_attack = line_index - 2
                    attack = Chessboard.rows[row_attack] + str(Chessboard.lines[line_attack]) # Attacked square on backward - left
                    result[attack] = None # Storing the attacked square in the result

            if row_index > 2: # Excluding knights on the 2 left edge rows
                if line_index < 8: # Excluding knights on the top edge
                    row_attack = row_index-2
                    line_attack = line_index+1
                    attack = Chessboard.rows[row_attack] + str(Chessboard.lines[line_attack]) # Attacked square on top - left
                    result[attack] = None # Storing the attacked square in the result
                
                if line_index > 1: # Excluding knights on the bottom edge
                    row_attack = row_index-2
                    line_attack = line_index-1
                    attack = Chessboard.rows[row_attack] + str(Chessboard.lines[line_attack]) # Attacked square on backward - left
                    result[attack] = None # Storing the attacked square in the result

            if row_index < 7: # Excluding knights on the 2 right edge rows
                if line_index < 8: # Excluding knights on the top edge
                    row_attack = row_index + 2
                    line_attack = line_index + 1
                    attack = Chessboard.rows[row_attack] + str(Chessboard.lines[line_attack]) # Attacked square on top - right
                    result[attack] = None # Storing the attacked square in the result
                
                if line_index > 1: # Excluding knights on the bottom edge
                    row_attack = row_index + 2
                    line_attack = line_index - 1
                    attack = Chessboard.rows[row_attack] + str(Chessboard.lines[line_attack]) # Attacked square on backward - right
                    result[attack] = None # Storing the attacked square in the result
                    
            if row_index < 8: # Excluding knights on the right edge
                if line_index < 7: # Excluding knights on the 2 top edge lines
                    row_attack = row_index + 1
                    line_attack = line_index + 2
                    attack = Chessboard.rows[row_attack] + str(Chessboard.lines[line_attack]) # Attacked square on top - right
                    result[attack] = None # Storing the attacked square in the result
                
                if line_index > 2: # Excluding knights on the 2 bottom edge lines
                    row_attack = row_index + 1
                    line_attack = line_index - 2
                    attack = Chessboard.rows[row_attack] + str(Chessboard.lines[line_attack]) # Attacked square on backward - right
                    result[attack] = None # Storing the attacked square in the result

        # Calculating the attacked squares if the piece is a Queen
        if square.piece.piece_type == 'Q':
            
            # Attacked squares front-right of the queen :
            if row_index < 8 and line_index < 8 : 
                row_index += 1
                line_index += 1
                
                while self.get_piece(row_index, line_index) == None and row_index < 8 and line_index < 8 : # Loop over the free squares front-right
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the attacked square
                    row_index += 1
                    line_index += 1 # Going to the next square

                attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result
                   
            # Attacked squares behind-right of the queen :
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes
            if row_index > 1 and line_index<8 :
                row_index -= 1
                line_index += 1
                
                while self.get_piece(row_index, line_index) == None and row_index > 1 and line_index < 8: # Loop over the free squares behind-right
                    attack=Chessboard.rows[row_index]+str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the attacked square
                    row_index -= 1
                    line_index += 1 # Going to the next square
                    
                attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result

            # Attacked squares front-left of the queen :
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes

            if row_index < 8 and line_index > 1:
                row_index += 1
                line_index -= 1
            
                while self.get_piece(row_index, line_index) == None and row_index < 8 and line_index > 1: # Loop over the free squares front-left
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the attacked square
                    row_index += 1
                    line_index -= 1 # Going to the next square
                    
                attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result

            # Attacked squares behind-left of the queen :
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes

            if row_index > 1 and line_index > 1:
                row_index -= 1
                line_index -= 1

                while self.get_piece(row_index, line_index) == None and row_index > 1 and line_index > 1: # Loop over the free squares behind-left
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the attacked square
                    line_index -= 1
                    row_index -= 1 # Going to the next square
                    
                attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result


            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes

            # Attacked squares in front of the queen :
            if row_index < 8:
                row_index += 1
                
                while self.get_piece(row_index, line_index) == None and row_index < 8: # Loop over the free squares in front
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the attacked square
                    row_index += 1 # Going to the next square

                attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result      
            
            # Attacked squares behind the queen :
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes
            if row_index > 1:
                row_index -= 1

                while self.get_piece(row_index, line_index) == None and row_index > 1: # Loop over the free squares behind
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the attacked square
                    row_index -= 1 # Going to the next square
                    
                attack = Chessboard.rows[row_index]+str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result 

            # Attacked squares on the right of the queen :
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes

            if line_index < 8:
                line_index += 1
            
                while self.get_piece(row_index, line_index) == None and line_index < 8: # Loop over the free squares on the right
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the attacked square
                    line_index += 1 # Going to the next square
                    
                attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result 

            # Attacked squares on the left of the queen :
            (row_index , line_index) = self.get_coord(square.name) # Reinitializing row and line indexes

            if line_index > 1:
                line_index -= 1

                while self.get_piece(row_index, line_index) == None and line_index > 1: # Loop over the free squares on the left
                    attack = Chessboard.rows[row_index] + str(Chessboard.lines[line_index])
                    result[attack] = None # Storing the attacked square
                    line_index -= 1 # Going to the next square
                    
                attack = Chessboard.rows[row_index]+str(Chessboard.lines[line_index]) # 1st square encountered with a piece on it
                result[attack] = None # Storing also this square in the result 

        # Removing the squares with pieces from the color which attacks
        erase_keys = {}
        for key in result.keys():
            try:
                if self.squares[key].piece.color == square.piece.color:
                    erase_keys[key] = None       
            except:
                pass
        for key in erase_keys.keys():
            del result[key]
            
        return result

    def all_attacks(self,color=None):
        """
        Returns a Dictionnary which keys are the squares references of the squares attacked by all the piece of a given color.
        Parameters
        ----------
            color : String
                The attacking color for which to get the attacked squares. If None, both colors are considered.
                Default is None.

        """
        result = {} # Initializing the result dictionnary
        for square in self.squares.values(): # Loop over all the squares of the Chessboard object
            if square.piece != None: # Excluding free squares
                if square.piece.color == color or color == None: # Excluding squares with a piece of the wrong color
                    attacks = self.attacks(square) # Storing all the squares attacked by this piece
                    result = {**result,**attacks} # Adding these squares to the result dictionnary
        return result

    def possible_moves(self,color):
        """
        Returns a list with all the possible moves references of a given color.
        Parameters
        ----------
            color : String
                The attacking color for which to get the possible moves.

        """
        result = [] # Initializing the result list
        for origin, square_origin in self.squares.items(): # Loop over all the square references of the chessboard object (tentative origin)
            if square_origin.piece != None: # Excluding free squares
                if square_origin.piece.color == color: # Excluding squares with a piece of the wrong color
                    for destination in self.squares.keys(): # Loop over all the square references of the chessboard object (tentative destination)
                        if self.is_valid(origin, destination, quiet=True, turn=False): # Check if a move to this destination is valid
                            if square_origin.piece.piece_type == 'P':
                                if origin[0] == destination[0]:
                                    result.append(destination) # Pawn regular move : the move reference is just the destination square
                                else:
                                    result.append(origin[0]+'x'+destination) # Pawn taking a piece : the move reference is of the form exd5 for example
                            else:
                                result.append(square_origin.piece.piece_type+origin[0]+destination) # Other piece types : Qe4 for example 


        if self.is_valid_castle(big = False, quiet = True):
            result.append('O-O') # Adding the castling move reference, if valid

        if self.is_valid_castle(big=True, quiet = True):
            result.append('O-O-O') # Adding the big castling move reference, if valid
            
        return result
               
    def is_checking(self,color):
        """
        Returns True if a player is currently 'checking' the opponent, for a given color of the player.
        Parameters
        ----------
            color : String
                The attacking color.

        """
        attacks = self.all_attacks(color) # Storing all the squares attacked by the player of the given color
        for key in attacks.keys(): # Loop over the attacked squares
            if self.squares[key].piece != None:
                if self.squares[key].piece.piece_type == 'K': # Check if the opponent king is in one of the attacked squares
                    return True
        return False

    def is_mating(self,color):
        """
        Returns True if a player is currently 'mating' the opponent, for a given color of the player.
        Parameters
        ----------
            color : String
                The attacking color.

        """

        if not self.is_checking(color): # If the player is not checking, it cannot be mating
            return False
        for ref, square in self.squares.items(): # Loop over all squares of the chessboard object (possible origin square of a move)
            if square.piece != None: # Excluding free squares
                if square.piece.color != color: # Excluding squares with pieces of the attacking color
                    for ref_test, square_test in self.squares.items(): # Loop over all squares of the chessboard object 
                                                                        # (possible destination squares of a move)
                        if self.is_valid(ref, ref_test, quiet=True, turn=False): # Excluding unvalid moves
                            test_board = copy.deepcopy(self) # Storing a copy of the chessboard object
                            test_board.cheat_move(ref, ref_test) # Moving the piece from origin to destination
                            if not test_board.is_checking(color): # Checking if the attacking color is still 'checking' after the move 
                                return False # If not, then the attacking color is not mating
        return True # If no move is found to avoid the attacking color to "check", then it's a "mat"
            
    def is_pating(self,color):
        """
        Returns True if a player is currently 'pating' the opponent, for a given color of the player.
        Parameters
        ----------
            color : String
                The attacking color.

        """
        if self.is_checking(color): # If the attacking player is "checking", then it is not pating
            return False
        for ref,square in self.squares.items(): # Loop over all squares of the chessboard object (possible origin square of a move)
            if square.piece != None: # Excluding free squares
                if square.piece.color != color: # Excluding squares with pieces of the attacking color
                    for ref_test, square_test in self.squares.items(): # Loop over all squares of the chessboard object 
                                                                        # (possible destination squares of a move)
                        if self.is_valid(ref, ref_test, quiet=True, turn=False): # Excluding unvalid moves
                            test_board = copy.deepcopy(self) # Storing a copy of the chessboard object
                            test_board.cheat_move(ref, ref_test) # Moving the piece from origin to destination
                            if not test_board.is_checking(color): # Checking if the attacking color is 'checking' after the move 
                                return False # If not, then there is no pat
        return True # If whatever the move, the opponent is "checked", then there is a "pat"

    def encode_fen(self):
        """
        Returns a string containing the Forsyth–Edwards Notation (FEN) of the current state of the chessboard.
        For more information on FEN : https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
        """
        fen = '' # Initializing the result string
       
        # 1/ Encoding the position of the pieces
        for line in range(8,0,-1): # Loop over the lines, from the top to bottom
            empty = 0 # Initializing the "free-squares" counter
            for row in [*'abcdefgh']: # Loop over the rows
                if self.squares[row+str(line)].piece != None: # If there is a piece on the square
                    if empty != 0: # If the previous cell was empty
                        fen = fen + str(empty) + str(self.squares[row+str(line)].piece) # Adding the count of free squares and then the piece
                        empty = 0 # Reinitializing the "free-squares" counter
                    else: # The previous cell had a piece
                        fen = fen + str(self.squares[row+str(line)].piece) # Just adding the piece
                else: # If there is no piece
                    empty += 1 # Increment the "free-squares" counter
            
            if empty != 0: # At the end of the line, check if we have free squares still in the counter
                fen = fen + str(empty) # If yes, adding the count of free squares
            if line != 1: # Checking if it was the last line
                fen = fen + '/' # If not, adding a '/'
        
        # 2/ Encoding the turn
        if self.turn == 'White':
            fen = fen + ' w '
        else:
            fen = fen + ' b '
        
        # 3/ Encoding the castling status
        no_castling = True
        if self.small_castle_white:
            fen = fen + 'K'
            no_castling = False
        if self.big_castle_white:
            fen = fen + 'Q'
            no_castling = False
        if self.small_castle_black:
            fen = fen + 'k'
            no_castling = False
        if self.big_castle_black:
            fen = fen + 'q'
            no_castling = False
        if no_castling: # Case if nobody can castle anymore
            fen = fen + '-'
        
        # 4/ Encoding the En-passant target square
        no_en_passant = True
        for row in [*'abcdefgh']: # Loop over the rows
            # Checking if black last move allows "en-passant"
            if self.previous == row +'7' + row + '5' and self.squares[row + '5'].piece.piece_type == 'P':  
                fen = fen + ' ' + row + '6'
                no_en_passant = False
            # Checking if white last move allows "en-passant"
            elif self.previous == row +'2' + row + '4' and self.squares[row + '4'].piece.piece_type == 'P':
                fen = fen + ' ' + row + '3'
                no_en_passant = False
        if no_en_passant: # Case if no "en-passant" is feasible
            fen = fen + ' -'

        # 5/ Encoding the "Half_move clock" information
        # To be correctly implemented but not critical. 0 can be used for now
        fen = fen + ' 0'

        # 6/ Encoding the Fullmove number information
        fen = fen + ' ' + str(self.count)

        return fen


