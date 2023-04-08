'''
Bots for Checker

Acknowledgement:
The strategy adopted by SmartBot was inspired by TA Joshua during the meeting.
'''
import random
import sys
sys.path.append("./logic")
import side
import board as BOARD
from board import PieceColor

import click

class RandomBot:
    '''
    Simple Bot that only moves at random
    '''
    
    def __init__(self, board, color):
        '''
        Constructor
        
        Args:
            board (CheckerBoard): the board the bot will be playing on
            color (str): Bot's color, either RED or BLACK
        '''
        self.board = board
        if color == 'RED':
            self.player = PieceColor.RED.value
        elif color == 'BLACK':
            self.player = PieceColor.BLACK.value
    
    def suggest_move(self):
        '''
        Suggests a random move

        Returns:
            initial_loc, chosen_loc (tuple[int]): initial location and chosen
                                                  location
        '''
        possible_pieces = list(self.board.possible_pieces(self.player))
        # randomly select a moveable piece
        selected_piece = random.choice(possible_pieces)

        possible_moves = self.board.possible_moves(selected_piece)
        # randomly select a possible move from the selected piece
        selected_move = random.choice(possible_moves)
        return selected_piece, selected_move

    def __str__(self):
        '''
        Returns a string representation of RandomBot

        Returns:
            type(str): type of RandomBot
        '''
        return "random"


class SmartBot:
    '''
    Smart Bot that implements a strategy to maximize its chance of winning.
    It will adopt the following strategy:
        - Take the move that will travel the longest distance. Usually this
          means the SmartBot will jump whenever possible and only moves if
          there's no way to jump
        - If the moves have the same distance, pick a random one
    '''
    
    def __init__(self, board, color):
        ''' 
        Constructor
        
        Args:
            board (CheckerBoard): the board the bot will be playing on
            color (str): Bot's color
        '''
        self.board = board
        if color == 'RED':
            self.player = PieceColor.RED.value
        elif color == 'BLACK':
            self.player = PieceColor.BLACK.value
    
    def suggest_move(self):
        '''
        Suggests a move according to the strategy

        Returns:
            initial_loc, chosen_loc (tuple[int]): initial location and chosen
                                                  location
        '''

        possible_pieces = list(self.board.possible_pieces(self.player))
        # shuffle all pieces and initialize best_piece to be the first one
        # this is because the best_piece will only get updated to a jump later
        # if there's one
        # if there's no better move, the next best_piece is always randomly
        # selected, which is consistent with the SmartBot's strategy
        random.shuffle(possible_pieces)
        best_piece = possible_pieces[0]
        best_move = self.board.possible_moves(best_piece)
        best_dist = -1

        for piece in possible_pieces:
            moves = self.board.possible_moves(piece)
            for move in moves:
                if len(move) > best_dist:
                    best_piece = piece
                    best_move = move
                    best_dist = len(move)

        return best_piece, best_move

    def __str__(self):
        '''
        Returns a string representation of SmartBot

        Returns:
            type(str): type of SmartBot
        '''
        return "smart"


#
# SIMULATION CODE
#
def initialize_players(player_type, board, color):
    '''
    A helper function to initialize the bot

    Args:
        player_type (str): the player's type, either random or smart
        board (CheckerBoard): the board the player will be playing on
        color (str): Bot's color, either RED or BLACK
    
    Returns:
        RandomBot or SmartBor: if player_type is random, returns a RandomBot
                                class object and similar for SmartBot
    '''
    if "random" in player_type.lower():
        return RandomBot(board, color)
    return SmartBot(board, color)

def simulate(n, players):
    """ 
    Simulates multiple games between two bots
    
    Args:
        n (int): The number of matches to play
        players (list[str]): a list of the types of the players
    
    Returns: 
        wins(int, int, int): number of wins for player1, player2 and ties
    """
    player1_wins, player2_wins, ties = 0, 0, 0
    for _ in range(n):
        board = BOARD.CheckerBoard(3)
        player1 = initialize_players(players[0], board, "RED")
        player2 = initialize_players(players[1], board, "BLACK")
        move_count = 0 

        current = player1

        while board.game_ended() == "CONTINUE":
            start_loc, chosen_loc = current.suggest_move()
            board.play(start_loc, chosen_loc)
            move_count += 1
            if move_count > 250:
                # When move_count is greater than 250, this is usually the edge
                # case where both players have only one piece left and it is
                # usually the king of each player
                # It cound end up in an infinite loop of game where neither king
                # could kill the other and ends up moving back and forth
                # We would end the game and count this as a tie
                break
            current = player2 if current == player1 else player1

        winner = board.game_ended()
        if "RED" in winner:
            player1_wins += 1
        elif "BLACK" in winner:
            player2_wins += 1
        else:
            ties += 1
        
    return player1_wins, player2_wins, ties


@click.command(name="checker-bot")
@click.option('-n', '--num-games',  type=click.INT, default=10000)
@click.option('--player1',
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
@click.option('--player2',
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="smart")
def cmd(num_games, player1, player2):
    bot1, bot2, ties = simulate(num_games, [player1, player2])

    print(f'Bot 1 ({player1}) wins: {100 * bot1 / num_games:.2f}%')
    print(f'Bot 2 ({player2}) wins: {100 * bot2 / num_games:.2f}%')
    print(f'Ties: {100 * ties / num_games:.2f}%')
    return

if __name__ == "__main__":
    cmd()