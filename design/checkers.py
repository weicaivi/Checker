from enum import Enum
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
        raise NotImplementedError

    def create_board(self):
        '''
        Create the board.
        '''
        raise NotImplementedError
    
    def __possible(self, loc):
        '''
        Test whether a location is a valid position within the board

        Args:
        loc: tuple(int, int): the row and col of the location to check

        Returns: bool: whether this location is valid
        '''
        raise NotImplementedError

    def initialize_board(self):
        '''
        Intializes the positions of the pieces for the board. Add correct pieces
        for each player.
        '''
        raise NotImplementedError
               
    def print_board(self):
        '''
        Prints the board for display in terminal.
        '''
        raise NotImplementedError
    
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
        raise NotImplementedError

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
        raise NotImplementedError

    def move(self, initial_loc, final_loc): 
        '''
        Move a piece from initial loc to final loc

        Args: 
            Initial_loc (tuple of int): location of the piece to be moved
            Final_loc (tuple of int): location the piece is to be moved to

        Raises:
            ValueError if move is invalid
        '''
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def game_ended(self):
        '''
        Return the winner if the game has been won
        
        Returns: str: whether someone has win 
        Possible returns: DRAW, BLACK WINS, RED WINS, CONTINUE
        '''
        raise NotImplementedError

    def __remove_piece(self, loc):
        '''
        Remove a piece from the board

        Inputs:
            loc: (list of tuple): the location of the piece to be removed

        Raises:
            ValueError if removal is invalid
        '''
        raise NotImplementedError

    def get_board_size(self):
        '''
        Returns size of the board (tuple of int)
        '''
        raise NotImplementedError

    def get_square(self, loc):
        '''
        Helper function. Returns a square at the specified loc.

        Inputs:
            loc (tuple of int): the location of the square to be obtained

        Returns: the square at the location (Square)
        '''
        raise NotImplementedError

    def get_piece(self, loc):
        '''
        Helper function. Returns a piece at the specified loc.

        Inputs:
            loc (tuple of int): the location of the piece to be obtained

        Returns: the piece at the location (Piece) or None if the location
            contains no piece
        '''
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def return_type(self):
        '''
        Returns type of the square.
        LIGHT for light square.
        DARK for empty dark square.
        RED / RED_KING for containing a regular/kinged red piece
        BLACK / BLACK_KING for containing a regular/kinged red piece
        '''
        raise NotImplementedError

    def empty(self):
        '''
        Empty the square of a piece

        Args:
            piece(object): Piece to be remove
        
        Raises: 
            ValueError if there is no piece contained in this square.
        '''
       raise NotImplementedError

class Side:
	'''
	The class is used to represent individual sides in the game.
	
	Public Attributes:
	Color (str): color representing this side
	pieces (set): set of pieces this side have
	'''
	
	def __init__(self, color):
		'''
		Constructor:
		Args: 
			color (PieceColor.color.value):  color of this side 
		'''
		# initialize the player for a new game
		self.color = color
		self.pieces = set()

	def get_moveable_pieces(self):
		'''
		If the player can jump, return all jumpable pieces. If not, return all
		pieces that can move diagnoally.
			
		Returns:
			set[tuple(row, column)]: set of location of pieces that are 
				moveable. Returns empty list if there is no movable piece.
		'''
		raise NotImplementedError

	def movable(self):
		'''
		Return whether the player can move

		Returns:
			Bool: whether the player can still move
		'''
		raise NotImplementedError
	
	def jumpable(self):
		'''
		Return whether the player can jump

		Returns:
			Bool: whether the player can still jump
		'''
		raise NotImplementedError
	
	def add_piece(self, piece):
		'''
		Add a piece to a player.

		Args:
			Piece (object): the piece to be added

		Raises:
			ValueError if piece is already in the list of pieces of the player
			
		Returns: None		
		'''
		raise NotImplementedError
	
	def remove_piece(self, piece):
		'''
		Remove a piece from the list of pieces of the player.

		Args:
			Piece (object): the piece to be removed

		Raises:
			ValueError if the player do not have this piece	
		
		Returns: None	
		'''
		raise NotImplementedError


class Piece:
    '''
    This class represents each individual checker piece on the board.

    Public Attributes:
    color (str): color of the piece
    square (Square): the square the piece is in
    is_king(bool): whether the piece is king
    board_size (int): the overall size of the board

    '''
    # these are the directions that can be explore going up/down
    UP_DIRS = ['up_left', 'up_right']
    DOWN_DIRS = ['down_left', 'down_right']
    ALL_DIRS = UP_DIRS + DOWN_DIRS

    def __init__(self, color, square, board_size):
        '''
        Constructor
        Initializes each piece

        Input:
        color[PieceColor.COLOR.value]: the color of the piece
        square[Square]: the square the color is in
        board_size[int]: the size of the board
        '''
        self.color = color
        self.square = square
        self.is_king = False
        self.board_size = board_size
    
    def return_loc(self):
        '''
        Returns the location of the piece (row, col) (tuple of int)
        '''
        raise NotImplementedError

    def get_possible_moves(self):
        '''
        Returns the possible moves of this piece.
        
        Return: 
        List[[tuple(int)]]]: a list of locations the piece can move to. Each
            location is inclosed as a list for parallel datatypes with jumps
        '''
        raise NotImplementedError

    def get_possible_jumps(self):
        '''
        Returns the possible jumps of this piece
        
        Return: 
        List[List[tuple of int]]: a list of possible jump path, each consisting
            of a list of locations of steps in the jump
        '''
        raise NotImplementedError

    def __possible_many_jumps(self, start_square, passed = []):
        '''
        Returns the possible jumps of this piece. This is helper function to be
        recursed over.
        
        Args:
            passed (list [tuple of ints]): the pieaces already jumped over

        Returns:
        List[List[tuple of int]]: a list of possible jump path, each consisting
            of a list of locations of steps in the jump
        '''
        raise NotImplementedError

    def __possible_one_jump(self,  start_square, passed = []):
        '''
        Returns possible one-step jumps of this piece. 
        
        Args:
            passed (list [tuple of ints]): the pieaces already jumped over

        Returns:
        List[tuple of int]: a list of possible jumped locations
        '''
        raise NotImplementedError

    def __test_dire(self, start_square, dire, opponent, passed):
        '''
        Test if a direction is valid for jumping

        Args:
            start_square(Square): the square to start the test
            dire (str): direction to test for jumping
            opponent (PieceColor.COLOR.value): colour of opponent
            passed (list [tuple of ints]): the pieaces already jumped over
        
        Return: bool: if the direction is valid for jumping
        '''
        raise NotImplementedError

    def step(self, desti, step_type):
        '''
        Move to a new location.

        Args:
            desti(Square): new location of the piece
            step_type(str): JUMP if this should be a jump, MOVE if this should
                be a move
        
        Raises:
            ValueError if step is not valid
        
        Return: None	
        '''
        raise NotImplementedError

    def __turns_king(self):
        '''
        Updates the status of the piece to become a king if it is not already
        one
                
        Return: None	
        '''
        raise NotImplementedError

