import pygame,sys,click
from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK"])
from logic.board import CheckerBoard
from mock_game import CheckerBoardStub
WIDTH = 800
HEIGHT = 800
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
selected = [-1,-1]
piece_exist=('r','b','R','B')
class GUIPlayer:
    """
    Simple class to store information about a GUI player
    A TUI player can either a human player using the keyboard,
    or a bot.
    """
    name: str
    def __init__(self, n: int, player_type: str, board,
                 color, opponent_color):
        """ Constructor
        Args:
            n: The player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            board: The Checker board
            color: The player's color
            opponent_color: The opponent's color
        """
        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        self.board = board
        self.color = color

def draw_board(board,screen,sizn,coln,moveable=None):
    """ Draws the current state of the board in the window
    Args:
        screen: Pygame surface to draw the board on
        board: The board to draw
        sizn: size of indivual square
        coln: number of rows and columns
        movable: all possible squares if any
    Returns: None
    """
    screen.fill(BLACK)
    for i in range(coln):
        for j in range(i % 2, coln, 2):
            pygame.draw.rect(screen, WHITE, (i*sizn, j*sizn, sizn, sizn))
    boardr = board.return_board()
    for i in range(coln):
        for j in range(coln):
            chr = boardr[i][j]
            if chr in piece_exist:
                if chr == 'r' or chr == 'R':
                    colort = RED
                else:
                    colort = BLACK
                center = (j * sizn + sizn // 2, i * sizn + sizn // 2)
                radius = sizn // 2.50
                radiusW = sizn //2.30
                pygame.draw.circle(screen, color=WHITE, center=center, radius=radiusW)
                pygame.draw.circle(screen, color=colort,center=center, radius=radius)
                if chr =='B' or chr == 'R':
                    center = (j * sizn + sizn // 2, i * sizn + sizn // 2.30)
                    radius = sizn // 2.50
                    radiusW = sizn //2.30
                    pygame.draw.circle(screen, color=WHITE,
                        center=center, radius=radiusW)
                    pygame.draw.circle(screen, color=colort,
                        center=center, radius=radius)     
    if moveable:
        for move in moveable:
            move1=move[0]
            move_x = move1[1]
            move_y = move1[0]
            pygame.draw.rect(screen, BLUE, (move_x*sizn, move_y*sizn, sizn, sizn))
    pygame.display.update() 

def splitloc(movable):
    """ Helper function to extract the first move from the list 
    Args:
        movable: list of all possible moves
    Returns: list of first step moes 
    """
    list1 = []
    for move in movable:
        list1.append(move[0])
    return list1

def select(screen, sizn, row, col,coln, board,current,selected):
    """
        function to let users select the piece at given position or execute the movement 
        screen: Pygame surface to draw the board on
        sizn: size of indivual square
        row: row that the player selected
        col: column that the player selected
        board: The board of play 
        sizn: size of indivual square
        coln: number of rows and columns
        current: current player color
        selected: track whether a piece have already been selected 
    """

    cur_pos=(row,col)
    if selected == [-1,-1]:
        list1 = board.possible_pieces(current.color.value)
        if cur_pos in list1:
            selected1 = [row,col]
            selected2 = (row,col)
            movable = board.possible_moves(selected2)
            draw_board(board,screen,sizn,coln, movable)
            return (selected1,False)
        else:
            draw_board(board,screen,sizn,coln)
            return([-1,-1],False)
    else:
        row1 = selected[0]
        col1 = selected[1]
        selected1=(row1,col1)
        cur_pos1=[row,col]
        piece1 = board.get_piece(selected1)
        flag = piece1.is_king
        movable = board.possible_moves(selected1)
        movable = splitloc(movable)
        if cur_pos in movable:
            if abs(selected[0]-cur_pos[0])==1:
                board.move(selected1,cur_pos)
            else:
                board.one_jump(selected1,cur_pos)
            movable = board.possible_jumps(cur_pos)   
            movable1 = splitloc(movable)
            movable2 = [movable1]
            if not flag and (cur_pos[0]==0 or cur_pos[0]==sizn-1):
                draw_board(board,screen,sizn,coln)
                return ([-1,-1],True)
            elif  abs(selected[0]-cur_pos[0])==2 and movable:
                '''print('Case',cur_pos1)'''
                draw_board(board,screen,sizn,coln, movable2)
                return(cur_pos1,False)
            else:
                draw_board(board,screen,sizn,coln)
                return ([-1,-1],True)
        return (selected,False)
    
def play_checker(board,players):
    """ Plays a game of Checker on a Pygame window
    Args:
        board: The board to play on
        players: A dictionary mapping piece colors to
          GUIPlayer objects.
    Returns: None
    """
    pygame.init()
    pygame.display.set_caption('Checkers')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    rown,coln= board.get_board_size()
    sizn = WIDTH//coln
    current = players[PieceColor.RED]
    draw_board(board,screen,sizn,coln)
    selected = [-1,-1]
    while board.game_ended()=='CONTINUE':
        clock.tick(24)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = pygame.mouse.get_pos()[0]
                y_pos = pygame.mouse.get_pos()[1]
                rowp = y_pos//sizn
                colp = x_pos//sizn
                temp = select(screen,sizn,rowp,colp,coln,board,current,selected)   
                selected = temp[0]
                flag = temp[1]
                if flag:
                    if current.color == PieceColor.BLACK:
                        current = players[PieceColor.RED]
                    elif current.color == PieceColor.RED:
                        current = players[PieceColor.BLACK]
    winner = board.game_ended()
    print(winner)

@click.command(name="Checkers-gui")
@click.option('--mode',
              type=click.Choice(['real', 'stub'], case_sensitive=False),
              default="real")
@click.option('--player1',
              type=click.Choice(['human'], case_sensitive=False),
              default="human")
@click.option('--player2',
              type=click.Choice(['human'], case_sensitive=False),
              default="human")
@click.option('--size',default=8)
def cmd(mode, player1, player2, size):
    if mode == "real":
        board = CheckerBoard((size-1)//2)
    elif mode == "stub":
        board = CheckerBoardStub((size-1)//2)
    player1 = GUIPlayer(1, player1, board, PieceColor.RED, PieceColor.BLACK)
    player2 = GUIPlayer(2, player2, board, PieceColor.BLACK, PieceColor.RED)
    players = {PieceColor.RED: player1, PieceColor.BLACK: player2}
    play_checker(board, players)

if __name__ == "__main__":
    cmd()
                


    

  
