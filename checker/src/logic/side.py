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
		# get all jumpable pieces
		movable_pieces = set()
		for piece in self.pieces:
			if piece.get_possible_jumps() != []:
				movable_pieces.add(piece.return_loc())

		# there are jumpable pieces, return those
		if len(movable_pieces) != 0:
			return movable_pieces

		# if not jumpable, get all pieces that can move diagonally and return
		# those
		for piece in self.pieces:
			if piece.get_possible_moves() != []:
				movable_pieces.add(piece.return_loc())
		return movable_pieces

	def movable(self):
		'''
		Return whether the player can move

		Returns:
			Bool: whether the player can still move
		'''
		return len(self.get_moveable_pieces()) != 0
	
	def jumpable(self):
		'''
		Return whether the player can jump

		Returns:
			Bool: whether the player can still jump
		'''
		# loop through each piece and test if they can jump
		for piece in self.self.pieces:
			if piece.get_possible_jumps() is not None:
				return True
		return False
	
	def add_piece(self, piece):
		'''
		Add a piece to a player.

		Args:
			Piece (object): the piece to be added

		Raises:
			ValueError if piece is already in the list of pieces of the player
			
		Returns: None		
		'''
		if piece not in self.pieces:
			self.pieces.add(piece)
		else:
			raise ValueError
	
	def remove_piece(self, piece):
		'''
		Remove a piece from the list of pieces of the player.

		Args:
			Piece (object): the piece to be removed

		Raises:
			ValueError if the player do not have this piece	
		
		Returns: None	
		'''
		if piece in self.pieces:
			self.pieces.remove(piece)
		else:
			raise ValueError
