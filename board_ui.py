import random, pygame, sys
from pygame.locals import *
from chessEngine import calcAllPositions, enemySide, determineCheck, determineCheckmate

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
BOXSIZE = 69
BOARDWIDTH = 8
BOARDHEIGHT = 8
XMARGIN = 45
YMARGIN = 45
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
        self.inCheck = False

    def calcNextMoves(self):
        moveList = []
        for piece in self.pieces:
            for move in piece.moveset:
                moveList.append(move)
        
        self.possibleNextMoves = moveList

    def checkStatus(self, enemy):
        self.inCheck = determineCheck(self, enemy)



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
        self.moveset = calcAllPositions(self.rank, 
                                        self.color, 
                                        self.board_pos, 
                                        board, 
                                        players)


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
        pygame.draw.rect(displaySurf, 
                        (0,255,102), 
                        pygame.Rect(left, top, BOXSIZE, BOXSIZE), 
                        3)
def reInitMoves(board):
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if board[i][j] != None:
                board[i][j].setMoves(board, players)

def drawBoard(board, displaySurf):
    background = pygame.image.load('img/board.png')
    displaySurf.blit(background, (0,0))
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if board[i][j] != None:
                board[i][j].draw(displaySurf)
                board[i][j].setMoves(board, players)

def drawPiece(piece, mousePos, displaySurf):
    pygame.mouse.set_visible(False)
    drawPos = (mousePos[0] - BOXSIZE/2, mousePos[1] - BOXSIZE/2)
    displaySurf.blit(piece.img, drawPos)

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

gameOver = False

while not gameOver:
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

    if pieceBeingHeld == True:
        drawBoard(board, DISPLAYSURF)
        drawMoves(controlledPiece.moveset, DISPLAYSURF)
        drawPiece(controlledPiece, (mousex,mousey), DISPLAYSURF)

    tile_x, tile_y = getTileAtPixel(mousex, mousey)
    if tile_x != None and tile_y != None:

        if mouseClicked:
        
            if pieceBeingHeld == False and board[tile_x][tile_y] != None and board[tile_x][tile_y].color == player:
                controlledPiece = board[tile_x][tile_y]
                board[tile_x][tile_y] = None
                pieceBeingHeld = True
                
            elif pieceBeingHeld and (tile_x,tile_y) in controlledPiece.moveset:
                board[tile_x][tile_y] = controlledPiece
                board[tile_x][tile_y].board_pos = (tile_x,tile_y)
                board[tile_x][tile_y].pixel_pos = coordToPixels(tile_x,tile_y)
                pieceBeingHeld = False

                reInitMoves(board)
                
                white.calcNextMoves()
                black.calcNextMoves()

                white.checkStatus(black)
                black.checkStatus(white)

                if determineCheckmate(black,white,board):
                    print("BLACK HAS BEEN CHECKMATED")
                    gameOver = True
                if determineCheckmate(white,black,board):
                    print("WHITE HAS BEEN CHECKMATED")
                    gameOver = True
                
                if white.inCheck:
                    print("WHITE IS IN CHECK")
                if black.inCheck:
                    print("BLACK IS IN CHECK")

                player = enemySide(player)
                print("it is now " + player + "'s turn")
                pygame.mouse.set_visible(True)

            elif pieceBeingHeld and (tile_x,tile_y) not in controlledPiece.moveset and (tile_x,tile_y) != controlledPiece.board_pos:
                print("Invalid move")
            
            elif pieceBeingHeld and (tile_x,tile_y) == controlledPiece.board_pos:
                pygame.mouse.set_visible(True)
                board[tile_x][tile_y] = controlledPiece
                board[tile_x][tile_y].board_pos = (tile_x,tile_y)
                board[tile_x][tile_y].pixel_pos = coordToPixels(tile_x,tile_y)
                pieceBeingHeld = False
                
            drawBoard(board, DISPLAYSURF)
        
    pygame.display.update()

print("Checkmate! Game over...")
