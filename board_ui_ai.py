import random, pygame, sys
from pygame.locals import *
from chessClasses import Player, Piece
from chessEngine import determineCheckmate, enemySide, nextBestMove, calcAllPositions, determineCheck, getStrength

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

#convert chess board coodinates to screen pixels
def coordToPixels( a,b ):
    x = (BOXSIZE * a) + XMARGIN
    y = (BOXSIZE * b) + YMARGIN
    
    return x,y

#I just realized that this probably does the same thing
def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE) + XMARGIN
    top = boxy * (BOXSIZE) + YMARGIN
    return (left, top)

#returns chess baord coordinate from pixels given
def getTileAtPixel(x,y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def pieceImgLoader(color,rank):
    return pygame.transform.scale(pygame.image.load('img/' + color + '_' + rank + '.png'), (PIECE_SIZE,PIECE_SIZE))

def move(board,piece,target):
    old_x,old_y = piece.board_pos
    x,y = target

    board[x][y] = piece
    board[x][y].board_pos = target
    board[x][y].pixel_pos = coordToPixels(x,y)

    board[old_x][old_y] = None

#sets up the board with pieces from each side
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

    for i in range(8):
        for j in range(8):
            if board[i][j] != None:
                if board[i][j].color == "white":
                    board[i][j].strength = getStrength(board[i][j].rank)
                else:
                    board[i][j].strength = -1 * getStrength(board[i][j].rank)

    return board

#draw possible moves to screen
def drawMoves(moves, displaySurf):
    for move in moves:
        left, top = leftTopCoordsOfBox(move[0],move[1])
        pygame.draw.rect(displaySurf, 
                        (0,255,102), 
                        pygame.Rect(left, top, BOXSIZE, BOXSIZE), 
                        3)

#reinitializes the moves for each player, piece
def reInitMoves(board):
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if board[i][j] != None:
                board[i][j].setMoves(calcAllPositions, board, players)

#draws the board and piece sprites
def drawBoard(board, displaySurf):
    background = pygame.image.load('img/board.png')
    displaySurf.blit(background, (0,0))
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if board[i][j] != None:
                board[i][j].img = pieceImgLoader(board[i][j].color,board[i][j].rank)
                board[i][j].draw(displaySurf)
                board[i][j].setMoves(calcAllPositions, board, players)

#draw piece at mouse position for "holding" effect
def drawPiece(piece, mousePos, displaySurf):
    pygame.mouse.set_visible(False)
    drawPos = (mousePos[0] - BOXSIZE/2, mousePos[1] - BOXSIZE/2)
    displaySurf.blit(piece.img, drawPos)

def trackPieces(board,white,black):
    white.pieces = []
    black.pieces = []
    for i in range(BOARDHEIGHT):
        for j in range(BOARDWIDTH):
            if board[i][j] != None:
                if board[i][j].color == "white":
                    white.pieces.append(board[i][j])
                else:
                    black.pieces.append(board[i][j])

def printPieceInfo(piece):
    print("rank: " + piece.rank)
    print("color: " + piece.color)
    print("protected?: " + str(piece.protected))

def updateGame(board,black,white):
    #recalc all the moves
    reInitMoves(board)
    
    white.calcNextTargets()
    black.calcNextTargets()

    #determine check and checkmate status
    white.checkStatus(determineCheck, black)
    black.checkStatus(determineCheck, white)

    if determineCheckmate(black,white,board):
        DISPLAYSURF.blit(checkmateTextImg, (0,0))
        print("BLACK HAS BEEN CHECKMATED")
    if determineCheckmate(white,black,board):
        DISPLAYSURF.blit(checkmateTextImg, (0,0))
        print("WHITE HAS BEEN CHECKMATED")
    if white.inCheck:
        print("WHITE IS IN CHECK")
    if black.inCheck:
        print("BLACK IS IN CHECK")

#setup pygame library
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Chess')

pickup_sound = pygame.mixer.Sound("sounds/pickup.wav")
putdown_sound = pygame.mixer.Sound("sounds/putdown.wav")

checkmateTextFont = pygame.font.SysFont('didot.ttc',72)
checkmateTextImg = checkmateTextFont.render('CHECKMATE', True, (255,0,0)) 
checkmateTextRect = checkmateTextImg.get_rect()
checkmateTextRect.center = ( WINDOWWIDTH // 2 , WINDOWWIDTH // 2 )

#set up players
white = Player([], [], "white")
black = Player([], [], "black")
players = [white, black]
white.calcNextTargets()
black.calcNextTargets()

#set up board matrix
board = []
for i in range(BOARDHEIGHT):
    row = []
    for j in range(BOARDWIDTH):
        row.append(None)
    board.append(row)

board = initBoard(board,DISPLAYSURF)
drawBoard(board, DISPLAYSURF)
trackPieces(board,white,black)

mousex = 0
mousey = 0
pieceBeingHeld = False

#first player is white
player = "white"

gameOver = False

#game loop starts
while True:
    gameOver = determineCheckmate(black,white,board) or determineCheckmate(white,black,board) 
    if gameOver:
        DISPLAYSURF.blit(checkmateTextImg,checkmateTextRect)
    else:
        mouseClicked = False

        if player == "black":

            (old,new) = nextBestMove(board,black,white,3)
            old_x,old_y = old

            move(board,board[old_x][old_y],new)

            pygame.mixer.Sound.play(putdown_sound)
            updateGame(board,black,white)
            
            player = "white"
            drawBoard(board, DISPLAYSURF)
            trackPieces(board,white,black)

        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True


            #get board tile where mouse is at
            tile_x, tile_y = getTileAtPixel(mousex, mousey)

            #if the chess piece is held, draw it on the board
            if pieceBeingHeld == True:
                drawBoard(board, DISPLAYSURF)
                drawMoves(controlledPiece.moveset, DISPLAYSURF)
                drawPiece(controlledPiece, (mousex,mousey), DISPLAYSURF)

            if tile_x != None and tile_y != None:

                if mouseClicked:
                    reInitMoves(board)
                    white.calcNextTargets()
                    black.calcNextTargets()

                    if(board[tile_x][tile_y] != None):
                        printPieceInfo(board[tile_x][tile_y])

                    if pieceBeingHeld == False and board[tile_x][tile_y] != None:
                        if board[tile_x][tile_y].color == player:
                            if not white.inCheck or white.inCheck and board[tile_x][tile_y].rank == 'king':
                                #piece is now picked up
                                controlledPiece = board[tile_x][tile_y]
                                board[tile_x][tile_y] = None
                                pieceBeingHeld = True

                        pygame.mixer.Sound.play(pickup_sound)

                    #if a piece is held and player clicked on a valid board spot
                    elif pieceBeingHeld and (tile_x,tile_y) in controlledPiece.moveset:
                        #place piece down
                        pygame.mixer.Sound.play(putdown_sound)
                        board[tile_x][tile_y] = controlledPiece
                        board[tile_x][tile_y].board_pos = (tile_x,tile_y)
                        board[tile_x][tile_y].pixel_pos = coordToPixels(tile_x,tile_y)
                        pieceBeingHeld = False

                        updateGame(board,black,white)

                        #flip player
                        player = enemySide(player)
                        print("it is now " + player + "'s turn")
                        pygame.mouse.set_visible(True)

                    #if piece is held and player clicks on original spot
                    elif pieceBeingHeld and (tile_x,tile_y) == controlledPiece.board_pos:
                        #place piece back at original position
                        pygame.mixer.Sound.play(putdown_sound)
                        pygame.mouse.set_visible(True)
                        board[tile_x][tile_y] = controlledPiece
                        board[tile_x][tile_y].board_pos = (tile_x,tile_y)
                        board[tile_x][tile_y].pixel_pos = coordToPixels(tile_x,tile_y)
                        pieceBeingHeld = False
                       
                    #draw board with new updates
                    drawBoard(board, DISPLAYSURF)
                    trackPieces(board,white,black)
            
    pygame.display.update()

print("Checkmate! Game over...")
