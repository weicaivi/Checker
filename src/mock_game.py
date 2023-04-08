# here are some useful commands for testing various functions in the game manually
class CheckerBoardStub:
    """
    Stub implementation of the ConnectMBoard class
    """
    def __init__(self, size=int):
        sizn = 800//8

        self.n = 8
        self._ncols = size 
        self._nrows = size 
        self._flag = False

    
    def game_ended(self):
        return 'Continue'
    
    def return_board(self):
        temp= [[''for i in range(self.n)]for j in range(self.n)]
        temp[0][1]='r'
        if self._flag == False:
            temp[7][2]='d'
        else:
            temp[6][3]='d'

        return temp


    def get_possible_pieces(self,current):

        return [(7,2)]
    
    def get_possible_move(self,current,pos):
        if pos == [7,2]:
            return [(6,3)]
        else:
            return []
    
    def move(self,current,pos):
        self._flag = True 
