from enum import Enum

PieceColor = Enum("PieceColor", ["RED", "BLACK"])

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
        return self.square.return_loc()

    def get_possible_moves(self):
        '''
        Returns the possible moves of this piece.
        
        Return: 
        List[[tuple(int)]]]: a list of locations the piece can move to. Each
            location is inclosed as a list for parallel datatypes with jumps
        '''
        moves = []
        # if it is a kinged_piece, test direction
        if self.is_king:
            for dire in Piece.ALL_DIRS:
                if self.square.connected[dire] and not \
                    self.square.connected[dire].occupied_by:
                    moves.append([self.square.connected[dire]])
        else:
            # if it is red, test only downwards
            if self.color == PieceColor.RED.value:
                for dire in Piece.DOWN_DIRS:
                    if self.square.connected[dire] and not \
                        self.square.connected[dire].occupied_by:
                        moves.append([self.square.connected[dire]])
            # if it is black, test only upwards
            else:
                for dire in Piece.UP_DIRS:
                    if self.square.connected[dire] and not \
                        self.square.connected[dire].occupied_by:
                        moves.append([self.square.connected[dire]])
        return [[move[0].return_loc()] for move in moves]  

    def get_possible_jumps(self):
        '''
        Returns the possible jumps of this piece
        
        Return: 
        List[List[tuple of int]]: a list of possible jump path, each consisting
            of a list of locations of steps in the jump
        '''
        return self.__possible_many_jumps(self.square)

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
        jumps = []
        for possible in self.__possible_one_jump(start_square, passed):
            row, col = possible.return_loc()
            if (row, col) not in passed:
                # if it is kinged at this step, stop at this jump
                if not self.is_king and possible.return_loc()[0] in \
                    [0, self.board_size - 1]:
                    jumps.append([possible.return_loc()])
                else:
                    i, j = start_square.return_loc()
                    further_jumps = self.__possible_many_jumps(possible, passed\
                        + [(int((i+row)/2), int((j+col)/2))])
                    # if there are no further jumps possible, stop at this jump
                    if not further_jumps:
                        jumps.append([possible.return_loc()])
                    else:
                        jumps = jumps + [([possible.return_loc()] + steps ) for\
                            steps in further_jumps]
        return jumps

    def __possible_one_jump(self,  start_square, passed = []):
        '''
        Returns possible one-step jumps of this piece. 
        
        Args:
            passed (list [tuple of ints]): the pieaces already jumped over

        Returns:
        List[tuple of int]: a list of possible jumped locations
        '''
        jumps = []
        # set opponent color
        if self.color == PieceColor.RED.value:
            opponent = PieceColor.BLACK.value
        else:
            opponent = PieceColor.RED.value
        
        # loop through
        if self.color == PieceColor.RED.value:
            for dire in Piece.DOWN_DIRS:
                if self.__test_dire(start_square, dire, opponent, passed):
                    jumps.append(start_square.connected[dire].connected[dire])          
            if self.is_king:
                for dire in Piece.UP_DIRS:
                    if self.__test_dire(start_square, dire, opponent, passed):
                        jumps.append(start_square.connected[dire].connected[dire])   
        else:
            for dire in Piece.UP_DIRS:
                if self.__test_dire(start_square, dire, opponent, passed):
                    jumps.append(start_square.connected[dire].connected[dire])          
            if self.is_king:
                for dire in Piece.DOWN_DIRS:
                    if self.__test_dire(start_square, dire, opponent, passed):
                        jumps.append(start_square.connected[dire].connected[dire])

        return jumps       

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
        if start_square.connected[dire] and \
            start_square.connected[dire].connected[dire] and \
            start_square.connected[dire].occupied_by and \
            start_square.connected[dire].occupied_by.color == opponent and \
            not start_square.connected[dire].connected[dire].occupied_by:
            row, col = start_square.connected[dire].connected[dire].return_loc()
            return start_square.connected[dire].return_loc() not in passed
        return False

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
        if step_type == 'MOVE':
            possible = [move[0] for move in self.get_possible_moves()]
        elif step_type == 'JUMP':
            possible = [jump.return_loc() for jump in \
                self.__possible_one_jump(self.square)]
        else:
            raise ValueError
        
        if desti.return_loc() in possible:
            self.square.empty()
            self.square = desti
            desti.add_piece(self)
            if desti.return_loc()[0] in [0, self.board_size - 1]:
                self.__turns_king()
        else:
            raise ValueError

    def __turns_king(self):
        '''
        Updates the status of the piece to become a king if it is not already
        one
                
        Return: None	
        '''
        if not self.is_king:
            self.is_king = True

