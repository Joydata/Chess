class Square:
    """
    A class to represent a Chessboard square.

    ...

    Attributes
    ----------
    name : str
        The reference of the Square object
    piece : Chesspiece object or None
        The Chesspiece positionned on this square, if any.

    Methods
    -------
    print_content(self):
        Prints the name of the square and its content.
    """

    def __init__(self,name,piece):
        """
        Instantiate a Square object.

        Parameters
        ----------
            name : str
                The reference of the Square object
            piece : Chesspiece object or None
                The Chesspiece positionned on this square, if any.
        """
        self.name=name
        self.piece=piece

    def __str__(self):
        """
        Called by the str() built-in function and by the print statement to compute the “informal” string representation 
        of the Square object

        """

        if self.piece != None:
            return '  __ \n |%s|' %(self.piece)
        else:
            return '.'

    def print_content(self):
        """
        Prints the name of the square and its content.

        """
        if self.piece!=None:
            print('%s : %s %s' % (self.name, self.piece.color, self.piece.piece_type))
        else:
            print('%s : empty' % (self.name))
