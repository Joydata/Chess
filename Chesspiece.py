class Chesspiece:
    """
    A class to represent a Chess piece.

    ...

    Attributes
    ----------
    piece_type : str
        The type of the chess piece
    color : str
        The color of the chess piece

    """

    Type_list = ['K','Q','R','N','B','P']
    Color_list = ['White','Black']
    pieces_dict = {'WhiteK':'K','WhiteQ':'Q','WhiteR':'R','WhiteB':'B','WhiteP':'P','WhiteN':'N','BlackK':'k','BlackQ':'q','BlackR':'r','BlackB':'b','BlackN':'n','BlackP':'p'}
    
    def __init__(self,piece_type,color):
        """
        Instantiate a Chesspiece object.

        Parameters
        ----------
            piece_type : str
                The type of the chess piece
                Must be one of ['K','Q','R','N','B','P']
            color : str
                The color of the chess piece
                Must be one of ['White','Black']
        """

        failed = False

        #Test if the piece_type parameter is in the right format
        if piece_type not in self.Type_list:
            print('The piece type must be one of ' + str(self.Type_list))
            failed = True
        
        #Test if the color parameter is in the right format
        if color not in self.Color_list:
            print('The color must be one of ' + str(self.Color_list))
            failed = True
        
        #Store the attributes if both piece_type and color parameters are in the right format
        if failed == False:
            self.piece_type = piece_type
            self.color = color

    def __str__(self):
        """
        Called by the str() built-in function and by the print statement to compute the “informal” string representation 
        of the Chesspiece object.
        Returns the piece_type attribute as
            - Uppercase if the color attribute of the Chesspiece object is 'White'
            - Lowercase if the color attribute of the Chesspiece object is 'Black'
        """
        if self.color == 'White':
            return self.piece_type
        else:
            return self.piece_type.lower()
