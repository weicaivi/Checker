from enum import Enum
from logic.side import Side
from logic.piece import Piece

PieceColor = Enum("PieceColor", ["RED", "BLACK"])
SquareType = Enum("SquareType", ["LIGHT", "DARK"])

class CheckerBoard:
    '''
    The class overseeing the overall game. 

    Public Atttributes: None
    '''

    def __init__(self, n = 3):
        '''
        Intializes the checker board

        Args:
        n (int): the number of rows of pieces for each player
        '''
        # we want to create pieces here then add the pieces to players when we 
        # initilalize the board below
        self.__size = 2 * n + 2
        #__players : two sides of the game labeled by color
        self.__players = {PieceColor.RED.value : Side('RED'), \
            PieceColor.BLACK.value : Side('BLACK')}
        # create the board and initalize pieces positions
        # private attribute: __board, __size
        self.create_board()
        self.initialize_board()

    def get_player_piece(self, player):
        '''
        Helper function for getting the locations of the pieces of a player

        Args:
        player (PieceColor.color.value): chosen player

        Returns: list[tuple(int, int)]: list of locations of each piece the
            player have
        '''
        player = self.__players[player]
        locs = []
        for piece in player.pieces:
            locs.append(piece.return_loc())
        return locs

    def create_board(self):
        '''
        Create the board.
        '''
        # construct the board
        self.__board = []
        for i in range(0, self.__size):
            row = []
            if i % 2 == 0:
                for j in range(0, self.__size):
                        if j % 2 == 0:
                            row.append(Square((i, j), SquareType.LIGHT.value))
                        else:
                            row.append(Square((i, j), SquareType.DARK.value))
            else:
                for j in range(0, self.__size):
                    if j % 2 == 1:
                        row.append(Square((i, j), SquareType.LIGHT.value))
                    else:
                        row.append(Square((i, j), SquareType.DARK.value))
            self.__board.append(row)

        # add connections between squares 
        # the goal is a graph we can iterate through
        for i in range(0, self.__size):
            for j in range(0, self.__size):
                square = self.__board[i][j]
                if self.__possible((i-1, j-1)):
                    square.connected['up_left'] = self.__board[i-1][j-1]
                if self.__possible((i-1, j+1)):
                    square.connected['up_right'] = self.__board[i-1][j+1]
                if self.__possible((i+1, j-1)):
                    square.connected['down_left'] = self.__board[i+1][j-1]
                if self.__possible((i+1, j+1)):
                    square.connected['down_right'] = self.__board[i+1][j+1]
    
    def __possible(self, loc):
        '''
        Test whether a location is a valid position within the board

        Args:
        loc: tuple(int, int): the row and col of the location to check

        Returns: bool: whether this location is valid
        '''
        row, col = loc
        return row >= 0 and row < self.__size and  col >= 0 and col < self.__size

    def initialize_board(self):
        '''
        Intializes the positions of the pieces for the board. Add correct pieces
        for each player.
        '''
        #clear pieces for both player
        for _, player in self.__players.items():
            player.pieces = set()

        #Loop through the dark squares of the board. Clear the square and add
        #the correct piece if needed
        for i in range(0, self.__size):
            for j in range(0, self.__size):
                square = self.__board[i][j]
                if square.return_type() != 'LIGHT':
                    square.empty()
                    if i < self.__size / 2 - 1:
                        piece = Piece(PieceColor.RED.value, square, self.__size)
                        self.__players[PieceColor.RED.value].add_piece(piece)
                        square.add_piece(piece)
                    elif i > self.__size / 2:
                        piece = Piece(PieceColor.BLACK.value, square, \
                            self.__size)
                        self.__players[PieceColor.BLACK.value].add_piece(piece)
                        square.add_piece(piece)
               
    def print_board(self):
        '''
        Prints the board for display in terminal.
        '''
        result = ''
        for i in range(self.__size):
            row = ''
            for j in range(self.__size):
                square = self.__board[i][j]
                if square.return_type() == 'LIGHT':
                    row = row + 'l'
                elif square.return_type() == 'DARK':
                    row = row + 'd'
                elif square.return_type() == "RED":
                    row = row + 'r'
                elif square.return_type() == "RED_KING":
                    row = row + 'R'
                elif square.return_type() == "BLACK_KING":
                    row = row + 'B'
                else:
                    row = row + 'b'
            result = result + '\n' + row
        print(result)
    
    def return_board(self):
        '''
        Returns workable version of the board, specifying only the types of
        squares (and types of pieces stored on the squares) in a 2D list. 

        Returns: list[list[str]]: A 2D list of types of each square. The types
            and string representation is specified below:
            l for light square
            d for empty dark square
            b & B for dark square with regular/kinged black piece
            r & R for dark square with regular/kinged red piece
        '''
        result = []
        for i in range(self.__size):
            row = []
            for j in range(self.__size):
                square = self.__board[i][j]
                if square.return_type() == 'LIGHT':
                    row.append('l')
                elif square.return_type() == 'BLACK':
                    row.append('b')
                elif square.return_type() == "RED":
                    row.append('r')
                elif square.return_type() == 'BLACK_KING':
                    row.append('B')
                elif square.return_type() == "RED_KING":
                    row.append('R')
                else:
                    row.append('d')
            result.append(row)
        return result

    def possible_pieces(self, player):
        '''
        Get all pieces that can be moved by the specified player 

        Args:
            player (PieceColor.COLOR.value): the player who selects a piece

        Raises: 
            ValueError if player is not valid

        Returns: set(tuple(int)): a set of locations of moveable pieces
        '''
        if player in self.__players:
            return self.__players[player].get_moveable_pieces()
        raise ValueError

    def possible_moves(self, loc):
        '''
        Get all possible moves of the piece selected.

        Args:
            loc (tuple(int)): the location of the selected piece
        
        Raises: 
            ValueError if location specified is not valid
        
        Returns:
            moves (list[tuple(int)]): a list of possible locations the piece can
                                      move to
        '''
        # get the piece
        row, col = loc
        try:
            piece = self.__board[row][col].occupied_by
            
            # if jumpable, ask for possible jumps; else, ask for possible moves
            possibles =  piece.get_possible_jumps()
            if possibles:
                return possibles
            return piece.get_possible_moves()
        except:
            raise ValueError

    def move(self, initial_loc, final_loc): 
        '''
        Move a piece from initial loc to final loc

        Args: 
            Initial_loc (tuple of int): location of the piece to be moved
            Final_loc (tuple of int): location the piece is to be moved to

        Raises:
            ValueError if move is invalid
        '''
        # get piece 
        i, j = initial_loc
        if self.__board[i][j].occupied_by is None:
            raise ValueError
        piece = self.__board[i][j].occupied_by

        # move to position
        row, col = final_loc
        #piece.move(self.__board[row][col])
        piece.step(self.__board[row][col], 'MOVE')

    def possible_jumps(self, loc):
        '''
        get all possible jumps of the specified piece 

        Args:
            loc (tuple(int)): the location of the selected piece
        
        Raises: 
            ValueError if location specified is not valid
        
        Returns:
            possibles (list[tuple(int)]): a list of possible locations the piece
                can jump to                       
        '''
        # get the piece
        row, col = loc
        try:
            piece = self.__board[row][col].occupied_by
        except:
            raise ValueError

        # if jumpable, ask for possible jumps; else, ask for possible moves
        possibles =  piece.get_possible_jumps()
        return possibles

    def one_jump(self, loc, step): 
        '''
        One step jump from loc to step.

        Caution: this function does not check if this jump is valid within a
        sequence of moves. For a complete sequence of jumps with validity 
        checks, use self.jump(). This function should only be used to loop
        through a sequence of jumps returned by possible jumps. 

        Args: 
            loc (tuple of int): location of the piece to be jumped
            step (tuple of int): location the piece is to be jumped to

        Raises:
            ValueError if move is invalid.
        '''
        # get the piece
        row, col = loc
        piece = self.__board[row][col].occupied_by

        # jump to location
        row1, col1 = step
        desti = self.__board[row1][col1]
        piece.step(desti, 'JUMP')
        removed = self.__board[int((row + row1) / \
            2)][int((col + col1)/2)].occupied_by
        self.__remove_piece(removed.return_loc())

    def jump(self, loc, steps): 
        '''
        Jump a piece from loc through a series of jump steps.

        Args: 
            loc (tuple of int): location of the piece to be jumped
            steps list[tuple of int]: list of locations for each step of the
                jump

        Raises:
            ValueError if jump is invalid
        '''
        # get the piece
        row, col = loc
        piece = self.__board[row][col].occupied_by

        # get valid jumps of the piece
        possibles =  piece.get_possible_jumps()

        # only attempt jump if whole sequence is valid
        if steps in possibles:
            for step in steps:
                # a single jump step
                row, col = piece.return_loc()
                row1, col1 = step
                desti = self.__board[row1][col1]
                piece.step(desti, 'JUMP')
                
                # remove the piece jumped over
                removed = self.__board[int((row + row1) / \
                    2)][int((col + col1)/2)].occupied_by
                self.__remove_piece(removed.return_loc())

        else:
            raise ValueError

    def game_ended(self):
        '''
        Return the winner if the game has been won
        
        Returns: str: whether someone has win 
        Possible returns: DRAW, BLACK WINS, RED WINS, CONTINUE
        '''
        # possibly replace this string flag with a better flag
        if not self.__players[PieceColor.RED.value].movable():
            if not self.__players[PieceColor.BLACK.value].movable():
                return 'DRAW'
            return 'BLACK WINS'
        elif not self.__players[PieceColor.BLACK.value].movable():
            return 'RED WINS'
        return 'CONTINUE'

    def __remove_piece(self, loc):
        '''
        Remove a piece from the board

        Inputs:
            loc: (list of tuple): the location of the piece to be removed

        Raises:
            ValueError if removal is invalid
        '''
        row, col = loc
        piece = self.__board[row][col].occupied_by
        self.__players[piece.color].remove_piece(piece)
        self.__board[row][col].empty()

    def get_board_size(self):
        '''
        Returns size of the board (tuple of int)
        '''
        return (self.__size,self.__size)

    def get_square(self, loc):
        '''
        Helper function. Returns a square at the specified loc.

        Inputs:
            loc (tuple of int): the location of the square to be obtained

        Returns: the square at the location (Square)
        '''
        i, j = loc
        return self.__board[i][j]

    def get_piece(self, loc):
        '''
        Helper function. Returns a piece at the specified loc.

        Inputs:
            loc (tuple of int): the location of the piece to be obtained

        Returns: the piece at the location (Piece) or None if the location
            contains no piece
        '''
        i, j = loc
        return self.__board[i][j].occupied_by

    def play(self, loc, steps):
        '''
        Move a piece from loc through a series of steps to a location. If it is
        a jumpable, it will always attempt a jump. If it is a move, the steps 
        would always be of length 1.

        Args: 
            loc (tuple of int): location of the piece to be jumped
            steps list[tuple of int]: list of locations for each step of the
                move

        Raises:
            ValueError if play is not valid.
        '''
        row, col = loc
        piece = self.__board[row][col].occupied_by
        
        jumps = piece.get_possible_jumps()
        if jumps != []:
            self.jump(loc, steps)
        else:
            if len(steps) == 1:
                self.move(loc, steps[0])
            else:
                raise ValueError

class Square:
    '''
    The class overseeing the a single square 

    Public Atttributes:
    row, col: (int): location of the square
    connected: dict{str : Square}: a dict mapping directions (up_left, down_left
    up_right, down_right) to the square on that direction. None if connection
    does not exist (because there is no square on that direction)
    '''
    def __init__(self, loc, color):
        '''
        Constructor 

        Args:
            loc: (tuple of int): location of the squqare
            color: SquareType.COLOR.value: the type of the square (Light or
                Dark)
            occupied_by: the piece occuping the square
        '''
        self.row, self.col = loc   
        self.connected = {key: None for key in ['up_left', 'down_left',\
             'up_right', 'down_right']}  
        self.occupied_by = None
        # the type of the square
        self.__type = color

    def return_loc(self):
        '''
        Returns the location of the square (row, col) (tuple of int)
        '''
        return (self.row, self.col)

    def add_piece(self, piece):
        '''
        Add a piece to a given Dark Square

        Args:
        piece(Piece): Piece to be added

        Raises: 
            ValueError if there is already a piece in the Square or if it is a
            light square

        Returns: None
        '''
        if self.return_type() == 'DARK':
            self.occupied_by = piece
        else:
            raise ValueError

    def return_type(self):
        '''
        Returns type of the square.
        LIGHT for light square.
        DARK for empty dark square.
        RED / RED_KING for containing a regular/kinged red piece
        BLACK / BLACK_KING for containing a regular/kinged red piece
        '''
        if self.__type == SquareType.LIGHT.value:
            return 'LIGHT'
        elif self.occupied_by is None:
            return 'DARK'
        elif self.occupied_by.color == PieceColor.RED.value:
            if self.occupied_by.is_king:
                return 'RED_KING'
            else:
                return 'RED'
        else:
            if self.occupied_by.is_king:
                return 'BLACK_KING'
            else:
                return 'BLACK'

    def empty(self):
        '''
        Empty the square of a piece

        Args:
            piece(object): Piece to be remove
        
        Raises: 
            ValueError if there is no piece contained in this square.
        '''
        if self.occupied_by is not None:
            self.occupied_by = None
