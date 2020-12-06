#Player class containing data on pieces, color, state
class Player:
    def __init__(self, pieces, moves, color):
        self.pieces = pieces
        self.possibleNextMoves = moves
        self.color = color
        self.inCheck = False

    #calculate next possible moves for player
    def calcNextMoves(self):
        moveList = []
        for piece in self.pieces:
            for move in piece.moveset:
                moveList.append(move)
        
        self.possibleNextMoves = moveList

    #sets player status wrt check or not in check
    def checkStatus(self, func, enemy):
        self.inCheck = func(self, enemy)


#Piece class containing data on spot, color, type
class Piece:
    def __init__(self, rank, color, pixel_pos, board_pos, moveset=None ):
        self.color = color
        self.rank = rank
        self.strength = 0
        self.protected = False
        self.img = None
        self.pixel_pos = pixel_pos
        self.board_pos = board_pos
        self.moveset = moveset
    
    #draws piece sprite to screen
    def draw(self, displaySurf):
        displaySurf.blit(self.img, self.pixel_pos)
   
    #calculates possible moves for piece
    def setMoves(self, func, board, players):
        self.moveset = func(self.rank, 
                            self.color, 
                            self.board_pos, 
                            board, 
                            players)
