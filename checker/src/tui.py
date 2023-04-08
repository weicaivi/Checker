from ast import literal_eval as make_tuple
import sys
sys.path.append("./logic")
from logic.board import CheckerBoard
from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK"])

class color:
   BLACK   = '\033[40m'
   WHITE   = '\033[47m'
   BLUE = '\033[94m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   END = '\033[0m'

def draw_board(board, select_pieces=False, select_moves=False):
    """
    Function that prints the current game board based on the data
    structure of return_board. Black pieces are represented in blue (for clarity & in
    consideration of potentially dark terminal background colors) and red pieces are 
    represented in red. Selected pieces are highlighted in yellow and potential moves
    are represented by a yellow '?'. 
    
    Input:
        board: list[list[str]]: a 2D list specifying only the type of each square
        select_pieces: tuple(int): the row and column of the selected piece
        select_moves: list[tuple(int)]: a list of final destination tuples the
        selected piece can move to
    
    Returns (str): the current game board
    """
    n = len(board)
    if n>9:
        result = ["   " + "0"*10+ "1"*(n-10) + "  "]
        result.append("   " + "".join(map(str, list(range(10)))) + \
                      "".join(map(str, list(range(n-10)))) + "   ")
        result.append("   +" + "-"*(n-2) + "+  ")
    else:
        result = ["  " + "".join(map(str, list(range(n)))) + "  "]
        result.append("  +" + "-"*(n-2) + "+  ")
    for x in range(n):
        if n>9 and x < 10:
            string = ("0%s|" % (x))
        else:
            string = ('%s|' % (x))
        for y in range(n):
            if select_pieces and ((x,y) in select_pieces or (x,y) == select_pieces):
                if board[x][y] == 'b':
                    string += color.YELLOW + 'b' + color.END
                elif board[x][y] == 'r':
                    string += color.YELLOW + 'r' + color.END
                elif board[x][y] == 'B':
                    string += color.YELLOW + 'B' + color.END
                elif board[x][y] == 'R':
                    string += color.YELLOW + 'R' + color.END
            elif select_moves and (x,y) in select_moves:
                string += color.YELLOW + '?' + color.END
            else:
                if board[x][y] == 'l':
                    string += color.WHITE + ' ' + color.END
                elif board[x][y] == 'b':
                    string += color.BLUE + 'b' + color.END
                elif board[x][y] == 'r':
                    string += color.RED + 'r' + color.END
                elif board[x][y] == 'B':
                    string += color.BLUE + 'B' + color.END
                elif board[x][y] == 'R':
                    string += color.RED + 'R' + color.END
                else:
                    string += color.BLACK + ' ' + color.END
        if n>9 and x < 10:
            string += ("|0%s" % (x))
        else:
            string += ('|%s' % (x))
        result.append(string)
    if n>9:
        result.append("   +" + "-"*(n-2) + "+  ")
        result.append("   " + "0"*10+ "1"*(n-10) + "  ")
        result.append("   " + "".join(map(str, list(range(10)))) + \
                      "".join(map(str, list(range(n-10)))) + "   ")
    else:
        result.append("  +" + "-"*(n-2) + "+  ")
        result.append("  " + "".join(map(str, list(range(n)))) + "  ")
        
    result = "\n".join(result)
    print(result)


def play(n):
    """
    Runs a game between two players, with the player in red starting first.

    Input: n (int): the size of the board

    Return: 
        Winner (str): whether if a winner is produced or the game ends in tie
        Current game board (str): the board after each player makes their move
    """
    eofg = False
    Board = CheckerBoard(int((n-2)/2))
    color = 'RED'
    while not eofg:
        winner = Board.game_ended()
        if winner != 'CONTINUE':
            print(winner, "!")
            eofg = True
        print()
        print('Current player: ', color)
        print()
        if color == 'RED':
            player = PieceColor.RED.value
        elif color == 'BLACK':
            player = PieceColor.BLACK.value
        possible_pieces = Board.possible_pieces(player)
        board = Board.return_board()
        draw_board(board,select_pieces=possible_pieces)
        print()
        start_loc = (0,0)
        while start_loc not in possible_pieces:
            start_loc = make_tuple(input(f"Which piece do you want to move? \
                                         (movable pieces are highlighted in yellow) \
                                         (Hint: one of {possible_pieces})"))
        possible_moves = Board.possible_moves(start_loc)
        final_dests = {}
        for idx, loc in enumerate(possible_moves):
            final_dests[idx] = loc[-1]
        print()
        draw_board(board,select_pieces=start_loc,select_moves=list(final_dests.values()))
        print()
        movement = (0,0)
        while movement not in list(final_dests.values()):
            movement = make_tuple(input(f"Where do you want to move it to? \
                (Hint: one of {list(final_dests.values())})"))
        print("The move is from: " + str(start_loc) + " to: " + str(movement))
        index = list(filter(lambda x: final_dests[x] == movement, final_dests))[0]
        Board.play(start_loc, possible_moves[index])
        if color == 'RED':
            color = 'BLACK'
        elif color == 'BLACK':
            color = 'RED'

def play_game():
    """
    Calls the previous functions to play a single game. 
    """
    n = 1
    while (n < 6 or n > 20) and n % 2 == 1:
        n = int(input("Size of the board? (Hint: input an even number from 6 to 20)"))
    print("Your input n is: " + str(n))
    play(n)


play_game()