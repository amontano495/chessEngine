import random, pygame, sys
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 640 # size of windows' height in pixels
BOXSIZE = 69
BOARDWIDTH = 8
BOARDHEIGHT = 8
XMARGIN = 46
YMARGIN = 46

GAP = 65
BORDER_WIDTH = 48

WHITE    = (255, 255, 255, 255)
BLACK    = (0, 0, 0, 255)

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
    

class Piece:
    def __init__(self, rank, color, pos, blank=True):
        self.color = color
        self.rank = rank
        self.img = pygame.image.load('img/' + color + '_' + rank + '.png')
        self.img = pygame.transform.scale(self.img, (65,65))
        self.pos = pos
        self.blank = blank


def initBoard(board, displaySurf):
    for i in range(8):
        board[i][1] = Piece("pawn","black", coordToPixels(i,1))
        board[i][6] = Piece("pawn","white", coordToPixels(i,6))
        displaySurf.blit(board[i][1].img, coordToPixels(i,1))
        displaySurf.blit(board[i][6].img, coordToPixels(i,6))
        board[i][1].blank = False
        board[i][6].blank = False

    for rank,i in zip(["rook","knight","bishop"], range(3)):
        board[i][0] = Piece(rank,"black", coordToPixels(i,0))
        board[i][7] = Piece(rank,"white", coordToPixels(i,7))
        displaySurf.blit(board[i][0].img, coordToPixels(i,0))
        displaySurf.blit(board[i][7].img, coordToPixels(i,7))
        board[i][0].blank = False
        board[i][7].blank = False
        
    for rank,i in zip(["bishop","knight","rook"], range(5,8)):
        board[i][0] = Piece(rank,"black", coordToPixels(i,0))
        board[i][7] = Piece(rank,"white", coordToPixels(i,7))
        displaySurf.blit(board[i][0].img, coordToPixels(i,0))
        displaySurf.blit(board[i][7].img, coordToPixels(i,7))
        board[i][0].blank = False
        board[i][7].blank = False


    for side,i in zip(["black","white"], [0,7]):
        board[4][i] = Piece("king",side, coordToPixels(4,i))
        board[3][i] = Piece("queen",side, coordToPixels(3,i))
        displaySurf.blit(board[4][i].img, coordToPixels(4,i))
        displaySurf.blit(board[3][i].img, coordToPixels(3,i))
        board[4][i].blank = False
        board[3][i].blank = False
        
    return board

def drawBoard(board, displaySurf):
    background = pygame.image.load('img/board.png')
    DISPLAYSURF.blit(background, (0,0))
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if board[i][j].blank == False:
                displaySurf.blit(board[i][j].img, board[i][j].pos)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
background = pygame.image.load('img/board.png')
DISPLAYSURF.blit(background, (0,0))
pygame.display.set_caption('Chess')

mousex = 0
mousey = 0

board = []
for i in range(8):
    row = []
    for j in range(8):
        row.append(Piece('rook','black',coordToPixels(i,j), True))
    board.append(row)

board = initBoard(board,DISPLAYSURF)
pieceBeingHeld = False


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
            if pieceBeingHeld == False and board[tile_x][tile_x].blank == False:
                print("piece picked up")
                controlledPiece = board[tile_x][tile_y]
                board[tile_x][tile_y].blank = True
                pieceBeingHeld = True

            elif pieceBeingHeld:
                print("piece put down")
                board[tile_x][tile_y] = controlledPiece
                board[tile_x][tile_y].pos = coordToPixels(tile_x,tile_y)
                board[tile_x][tile_y].blank = False
                pieceBeingHeld = False

            drawBoard(board, DISPLAYSURF)
            

        
    pygame.display.update()


