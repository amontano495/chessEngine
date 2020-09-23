import random, pygame, sys
from pygame.locals import *
from chessEngine import calcAllPositions, enemySide

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
BOXSIZE = 69
BOARDWIDTH = 8
BOARDHEIGHT = 8
XMARGIN = 46
YMARGIN = 46
PIECE_SIZE = 65
BORDER_WIDTH = 48

def coordToPixels( a,b ):
    x = (BOXSIZE * a) + XMARGIN
    y = (BOXSIZE * b) + YMARGIN
    
    return x,y
    
def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE) + XMARGIN
    top = boxy * (BOXSIZE) + YMARGIN
    return (left, top)
    
def getTileAtPixel(x,y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

class Player:
    def __init__(self, pieces, moves, color):
        self.pieces = pieces
        self.possibleNextMoves = moves
        self.color = color

    def calcNextMoves(self):
        moveList = []
        for piece in self.pieces:
            for move in piece.moveset:
                moveList.append(move)
        
        self.possibleNextMoves = moveList


class Piece:
    def __init__(self, rank, color, pixel_pos, board_pos, moveset=None):
        self.color = color
        self.rank = rank
        self.img = pygame.image.load('img/' + color + '_' + rank + '.png')
        self.img = pygame.transform.scale(self.img, (PIECE_SIZE,PIECE_SIZE))
        self.pixel_pos = pixel_pos
        self.board_pos = board_pos
        self.moveset = moveset
     
    def draw(self, displaySurf):
        displaySurf.blit(self.img, self.pixel_pos)
    
    def setMoves(self, board, players):
        self.moveset = calcAllPositions(self.rank, self.color, self.board_pos, board, players)


def initBoard(board, displaySurf):
    for i in range(8):
        board[i][1] = Piece("pawn","black", coordToPixels(i,1), (i,1))
        board[i][6] = Piece("pawn","white", coordToPixels(i,6), (i,6))

    for rank,i in zip(["rook","knight","bishop"], range(3)):
        board[i][0] = Piece(rank,"black", coordToPixels(i,0), (i,0))
        board[i][7] = Piece(rank,"white", coordToPixels(i,7), (i,7))
        
    for rank,i in zip(["bishop","knight","rook"], range(5,8)):
        board[i][0] = Piece(rank,"black", coordToPixels(i,0), (i,0))
        board[i][7] = Piece(rank,"white", coordToPixels(i,7), (i,7))


    for side,i in zip(["black","white"], [0,7]):
        board[4][i] = Piece("king",side, coordToPixels(4,i), (4,i))
        board[3][i] = Piece("queen",side, coordToPixels(3,i), (3,i))
        
    return board

def drawMoves(moves, displaySurf):
    for move in moves:
        left, top = leftTopCoordsOfBox(move[0],move[1])
        pygame.draw.rect(displaySurf, (255,0,0), pygame.Rect(left, top, BOXSIZE, BOXSIZE), 1)

def drawBoard(board, displaySurf):
    background = pygame.image.load('img/board.png')
    displaySurf.blit(background, (0,0))
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if board[i][j] != None:
                board[i][j].draw(displaySurf)
                board[i][j].setMoves(board, players)
                drawMoves(board[i][j].moveset, displaySurf)


pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Chess')

#set up players
white = Player([], [], "white")
black = Player([], [], "black")
players = [white, black]
white.calcNextMoves()
black.calcNextMoves()

board = []
for i in range(BOARDHEIGHT):
    row = []
    for j in range(BOARDWIDTH):
        row.append(None)
    board.append(row)

board = initBoard(board,DISPLAYSURF)
drawBoard(board, DISPLAYSURF)

for i in range(BOARDHEIGHT):
    for j in range(BOARDWIDTH):
        if board[i][j] != None:
            if board[i][j].color == "white":
                white.pieces.append(board[i][j])
            else:
                black.pieces.append(board[i][j])

#print(white.possibleNextMoves)
mousex = 0
mousey = 0
pieceBeingHeld = False

player = "white"

while True:
    mouseClicked = False
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            mouseClicked = True

    tile_x, tile_y = getTileAtPixel(mousex, mousey)
    if tile_x != None and tile_y != None:

        if mouseClicked:
        
            if pieceBeingHeld == False and board[tile_x][tile_y] != None and board[tile_x][tile_y].color == player:
                controlledPiece = board[tile_x][tile_y]
                board[tile_x][tile_y] = None
                pieceBeingHeld = True
                print("POSSIBLE MOVES: " + str(controlledPiece.moveset))
                
            elif pieceBeingHeld and (tile_x,tile_y) in controlledPiece.moveset:
                board[tile_x][tile_y] = controlledPiece
                board[tile_x][tile_y].board_pos = (tile_x,tile_y)
                board[tile_x][tile_y].pixel_pos = coordToPixels(tile_x,tile_y)
                pieceBeingHeld = False
                
                player = enemySide(player)
                print("it is now " + player + "'s turn")

            elif pieceBeingHeld and (tile_x,tile_y) not in controlledPiece.moveset and (tile_x,tile_y) != controlledPiece.board_pos:
                print("Invalid move")
            
            elif pieceBeingHeld and (tile_x,tile_y) == controlledPiece.board_pos:
                board[tile_x][tile_y] = controlledPiece
                board[tile_x][tile_y].board_pos = (tile_x,tile_y)
                board[tile_x][tile_y].pixel_pos = coordToPixels(tile_x,tile_y)
                pieceBeingHeld = False
                
            drawBoard(board, DISPLAYSURF)
        
    pygame.display.update()