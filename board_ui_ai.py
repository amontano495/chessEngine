import random, pygame, sys
from pygame.locals import *
from chessEngine import calcAllPositions, enemySide, determineCheck, determineCheckmate, getStrength, nextBestMove

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
    def checkStatus(self, enemy):
        self.inCheck = determineCheck(self, enemy)


#Piece class containing data on spot, color, type
class Piece:
    def __init__(self, rank, color, pixel_pos, board_pos, moveset=None):
        self.color = color
        self.rank = rank
        self.strength = getStrength(self.rank)
        self.protected = False
        self.img = pygame.image.load('img/' + color + '_' + rank + '.png')
        self.img = pygame.transform.scale(self.img, (PIECE_SIZE,PIECE_SIZE))
        self.pixel_pos = pixel_pos
        self.board_pos = board_pos
        self.moveset = moveset
    
    #draws piece sprite to screen
    def draw(self, displaySurf):
        displaySurf.blit(self.img, self.pixel_pos)
   
    #calculates possible moves for piece
    def setMoves(self, board, players):
        self.moveset = calcAllPositions(self.rank, 
                                        self.color, 
                                        self.board_pos, 
                                        board, 
                                        players)

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
                board[i][j].setMoves(board, players)

#draws the board and piece sprites
def drawBoard(board, displaySurf):
    background = pygame.image.load('img/board.png')
    displaySurf.blit(background, (0,0))
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if board[i][j] != None:
                board[i][j].draw(displaySurf)
                board[i][j].setMoves(board, players)

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
white.calcNextMoves()
black.calcNextMoves()

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
    if gameOver:
        DISPLAYSURF.blit(checkmateTextImg,checkmateTextRect)
    else:
        mouseClicked = False

        if player == "black":

            (old,new) = nextBestMove(board,black)
            old_x,old_y = old
            new_x,new_y = new
            print(old)

            blackPiece = board[old_x][old_y]

            board[new_x][new_y] = blackPiece
            board[new_x][new_y].board_pos = (new_x,new_y)
            board[new_x][new_y].pixel_pos = coordToPixels(new_x,new_y)

            board[old_x][old_y] = None

            pygame.mixer.Sound.play(putdown_sound)
            reInitMoves(board)
            
            white.calcNextMoves()
            black.calcNextMoves()

            #determine check and checkmate status
            white.checkStatus(black)
            black.checkStatus(white)

            if determineCheckmate(black,white,board):
                DISPLAYSURF.blit(checkmateTextImg, (0,0))
                print("BLACK HAS BEEN CHECKMATED")
                gameOver = True
            if determineCheckmate(white,black,board):
                DISPLAYSURF.blit(checkmateTextImg, (0,0))
                print("WHITE HAS BEEN CHECKMATED")
                gameOver = True
            
            if white.inCheck:
                print("WHITE IS IN CHECK")
            if black.inCheck:
                print("BLACK IS IN CHECK")
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
                    white.calcNextMoves()
                    black.calcNextMoves()

                    if(board[tile_x][tile_y] != None):
                        printPieceInfo(board[tile_x][tile_y])

                    #if a piece is not being held and player clicked on a piece that belongs to them
                    if pieceBeingHeld == False and board[tile_x][tile_y] != None and board[tile_x][tile_y].color == player and not white.inCheck:
                        #piece is now picked up
                        controlledPiece = board[tile_x][tile_y]
                        board[tile_x][tile_y] = None
                        pieceBeingHeld = True
                        pygame.mixer.Sound.play(pickup_sound)
                       
                    elif pieceBeingHeld == False and board[tile_x][tile_y] != None and board[tile_x][tile_y].color == player and board[tile_x][tile_y].rank == 'king' and white.inCheck:
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

                        #recalc all the moves
                        reInitMoves(board)
                        
                        white.calcNextMoves()
                        black.calcNextMoves()

                        #determine check and checkmate status
                        white.checkStatus(black)
                        black.checkStatus(white)

                        if determineCheckmate(black,white,board):
                            DISPLAYSURF.blit(checkmateTextImg, (0,0))
                            print("BLACK HAS BEEN CHECKMATED")
                            gameOver = True
                        if determineCheckmate(white,black,board):
                            DISPLAYSURF.blit(checkmateTextImg, (0,0))
                            print("WHITE HAS BEEN CHECKMATED")
                            gameOver = True
                        
                        if white.inCheck:
                            print("WHITE IS IN CHECK")
                        if black.inCheck:
                            print("BLACK IS IN CHECK")

                        #flip player
                        player = enemySide(player)
                        print("it is now " + player + "'s turn")
                        pygame.mouse.set_visible(True)

                    #if a piece is held and player tries to click on invalid spot
                    elif pieceBeingHeld and (tile_x,tile_y) not in controlledPiece.moveset and (tile_x,tile_y) != controlledPiece.board_pos:
                        print("Invalid move")
                   
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
