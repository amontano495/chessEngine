#CLass definition for piece object
class Piece:
    def __init__(self, rank, player, position, possibleMoves):
        #rank: King, Queen, Knight, etc
        self.rank = rank
        #White or Black
        self.player = player
        #tuple of position on board
        self.position = position
        #list of positions available to piece
        self.possibleMoves = possibleMoves


whiteSide = []
blackSide = []

#global board matrix
#list of list of Piece objects
board = []
for i in range(8):
    row = []
    for j in range(8):
        row.append(Piece("EMPTY","NONE",(i,j),[]))
    board.append(row)

#determines if tuple is outside of board limits
def outOfBounds(position):
    if (position[0] >= 0 and position[0] <= 7) and (position[1] >= 0 and position[1] <= 7):
        return False
    return True

#returns opposite of given player string
def enemySide(player):
    if player == "white":
        return "black"
    else:
        return "white"

def pawnPositions(rank, color, position, board, players):
    positionsList = []

    #black pieces move down the board, white pieces move up
    direction = 1 if color == "black" else -1

    diagLeft = (position[0] - 1, position[1] + direction)
    diagRight = (position[0] + 1, position[1] + direction)

    #if there is no enemy directly in front
    if board[position[0]][position[1] + direction] == None:
        #pawn is able to move forward
        moveForward = (position[0], position[1] + direction)
        positionsList.append(moveForward)

    #pawn can move diagonally if enemy present
    for move in [diagLeft, diagRight]:
        if outOfBounds(move) == False:
            tile = board[move[0]][move[1]]
            if tile != None:
                if tile.color == enemySide(color):
                    positionsList.append(move)

    #at initial move, pawn can move two tiles
    if (position[1] == 6 and color == "white") or (position[1] == 1 and color == "black"):
        positionsList.append((position[0] , position[1] + direction*2))
    
    return positionsList

def knightPositions(rank, color, position, board, players):
    positionsList = []

    positionsList.append((position[0] + 1, position[1] + 2))
    positionsList.append((position[0] - 1, position[1] + 2))
    positionsList.append((position[0] + 1, position[1] - 2))
    positionsList.append((position[0] - 1, position[1] - 2))
    
    positionsList.append((position[0] + 2, position[1] + 1))
    positionsList.append((position[0] - 2, position[1] + 1))
    positionsList.append((position[0] + 2, position[1] - 1))
    positionsList.append((position[0] - 2, position[1] - 1))
            
    return positionsList


def bishopPositions(rank, color, position, board, players):
    positionsList = []

    upLeft = position
    upRight = position
    downLeft = position
    downRight = position

    upLeftPath = []
    upRightPath = []
    downLeftPath = []
    downRightPath = []

    for i in range(8):
        upLeft = (upLeft[0] - 1, upLeft[1] - 1)
        upLeftPath.append(upLeft)

        upRight = (upRight[0] + 1, upRight[1] - 1)
        upRightPath.append(upRight)

        downLeft = (downLeft[0] - 1, downLeft[1] + 1)
        downLeftPath.append(downLeft)

        downRight = (downRight[0] + 1, downRight[1] + 1)
        downRightPath.append(downRight)

    upLeftPath = rookHelper(upLeftPath, color, board)
    upRightPath = rookHelper(upRightPath, color, board)
    downLeftPath = rookHelper(downLeftPath, color, board)
    downRightPath = rookHelper(downRightPath, color, board)

    positionsList = upLeftPath + upRightPath + downLeftPath + downRightPath

    return positionsList

def rookHelper(pathList, color, board):
    count = 0
    newPath = pathList
    for pos in pathList:
        count += 1
        (x,y) = pos
        if not outOfBounds(pos):
            if board[x][y] != None:
                newPath = pathList[:count]
                break
    return newPath

def rookPositions(rank, color, position, board, players):
    positionsList = []

    horizontal = []
    vertical = []
    for i in range(8):
        if (i,position[1]) != position:
            horizontal.append((i,position[1]))
        if (position[0],i) != position:
            vertical.append((position[0], i))

    up = []
    down = []
    for pos in vertical:
        if pos[1] < position[1]:
            up.append(pos)
        elif pos[1] > position[1]:
            down.append(pos)
    up.reverse()

    left = []
    right = []    
    for pos in horizontal:
        if pos[0] < position[0]:
            left.append(pos)
        elif pos[0] > position[0]:
            right.append(pos)
    left.reverse()

    up = rookHelper(up, color, board)
    down = rookHelper(down, color, board)
    left = rookHelper(left, color, board)
    right = rookHelper(right, color, board)

    positionsList = left + right + up + down

    return positionsList

def queenPositions(rank, color, position, board, players):
    orthogonalMoves = rookPositions(rank, color, position, board, players)
    diagonalMoves = bishopPositions(rank, color, position, board, players)

    positionsList = orthogonalMoves + diagonalMoves
    
    return positionsList

def kingPositions(rank, color, position, board, players):
    positionsList = []

    topleft = ( position[0]  - 1, position[1] - 1 )
    botright = ( position[0]  + 1, position[1] + 1 )

    if color == "white":
        possibleEnemyPositions = players[1].possibleNextMoves
    else:
        possibleEnemyPositions = players[0].possibleNextMoves
    
    #print(possibleEnemyPositions)

    for i in range(topleft[0], botright[0] + 1):
        for j in range(topleft[1], botright[1] + 1):
            if (i,j) != position and not outOfBounds((i,j)) and (i,j) not in possibleEnemyPositions:
                positionsList.append( (i,j) )

    return positionsList


#calculates possible moves for given piece
def calcAllPositions(rank, color, position, board, players):
    positionsList = []

    #if piece is a knight, all "L" positions added to list
    if rank == "knight":
        positionsList = knightPositions(rank, color, position, board, players)

    #if piece is a pawn
    elif rank == "pawn":
        positionsList = pawnPositions(rank, color, position, board, players)

    #if piece is a king
    elif rank == "king":
        positionsList = kingPositions(rank, color, position, board, players)

    #if piece is a queen
    elif rank == "queen":
        positionsList = queenPositions(rank, color, position, board, players)

    #if piece is a rook
    elif rank == "rook":
        positionsList = rookPositions(rank, color, position, board, players)

    #if piece is a bishop
    elif rank == "bishop":
        positionsList = bishopPositions(rank, color, position, board, players)

    #remove any out of bounds positions
    positionsList = list(filter(lambda tup: (tup[0] < 8 and tup[0] >= 0) and (tup[1] < 8 and tup[1] >= 0),positionsList))


    invalidPosList = []
    #remove positions with pieces on board of same side
    for pos in positionsList:
        try:
            if board[pos[0]][pos[1]].color == color:
                invalidPosList.append(pos)
        except AttributeError:
            pass

    positionsList = list(set(positionsList) - set(invalidPosList))

    return positionsList

#determines if move is acceptable by standard chess rules    
def validMove(piece, target, player):
    #check if piece being moved is owned by player
    correctPlayer = piece.player == player

    #calculate all possible moves for piece
    possiblePositions = calcAllPositions(piece)

    #if piece is owned by player and target is in move list
    if correctPlayer and (target in possiblePositions):
        return True
    else:
        return False

#moves piece to target position on board
def move(piece, target, player):
    print(piece.possibleMoves)
    if validMove(piece, target, player):
        #replace previous position with empty
        board[piece.position[0]][piece.position[1]] = Piece("EMPTY","NONE",piece.position,[])

        #update piece position
        piece.position = target

        #update board position at target to piece
        board[target[0]][target[1]] = piece
        print(player + " MOVES " + piece.rank + " TO " + str(target))
        return True
    else:
        print("INVALID MOVE")
        return False

#function to draw board contents to screen
def drawBoard():
    print('#'*24)
    for i in range(8):
        row = str(8 - i) + "  " + '|'
        for j in range(8):
            cell = board[j][i]
            if cell.rank == "EMPTY":
                row = row + "  " + '|'
            else:
                row = row + cell.player[0] + cell.rank[0] + '|'
        print(row)
        print('-'*27)
    print("   |A |B |C |D |E |F |G |H ")

#initializes the board, adds default pieces
def initBoard():
    #pawns
    for i in range(8):
        board[i][1] = Piece("PAWN","BLACK",(i,1),[])
        blackSide.append(board[i][1])

        board[i][6] = Piece("PAWN","WHITE",(i,6),[])
        whiteSide.append(board[i][6])

    for rank,i in zip(["ROOK","KNIGHT","BISHOP"], range(3)):
        board[i][0] = Piece(rank,"BLACK",(i,0),[])
        blackSide.append(board[i][0])

        board[i][7] = Piece(rank,"WHITE",(i,7),[])
        whiteSide.append(board[i][7])

    for rank,i in zip(["BISHOP","KNIGHT","ROOK"], range(5,8)):
        board[i][0] = Piece(rank,"BLACK",(i,0),[])
        blackSide.append(board[i][0])

        board[i][7] = Piece(rank,"WHITE",(i,7),[])
        whiteSide.append(board[i][7])

    for side,i in zip(["BLACK","WHITE"], [0,7]):
        board[4][i] = Piece("kING",side,(4,i),[])        
        board[3][i] = Piece("QUEEN",side,(3,i),[])        

        if side == "WHITE":
            whiteSide.append(board[3][i])
            whiteSide.append(board[4][i])

        if side == "BLACK":
            blackSide.append(board[3][i])
            blackSide.append(board[4][i])

    #calculate possible moves for each piece on board
    for i in range(8):
        for j in range(8):
                board[i][j].possibleMoves = calcAllPositions(board[i][j])

alphabet = "ABCDEFGH"
coordDict = {alphabet[i] : i for i in list(range(8))}

def updatePieceMoves():
    for i in range(8):
        for j in range(8):
                board[i][j].possibleMoves = calcAllPositions(board[i][j])

#converts algebraic notation to numeric tuples
def anToMat(coords):
    xcoord = int(coordDict[coords[0]])
    ycoord = 8 - int(coords[1])

    return (xcoord,ycoord)

#gets king from side
def getKing(side):
    for i in range(8):
        for j in range(8):
            if board[i][j].rank == "kING" and board[i][j].player == side:
                return board[i][j]

#determines if a king is in check
def determineCheck(player, enemy_player):
    for piece in player.pieces:
        if piece.rank == "king":
            king = piece

    if king.board_pos in enemy_player.possibleNextMoves:
        return True

    return False

#determines if game is in checkmate
def determineCheckmate():
    pieceVector = [piece for row in board for piece in row]
    for side in ["WHITE","BLACK"]:
        king = getKing(side)
        enemyPieces = [piece for piece in pieceVector if piece.player == enemySide(side)]

        allPossibleEnemyMoves = []
        for piece in enemyPieces:
            allPossibleEnemyMoves.append(piece.possibleMoves)


        print(side)
        print("KING MOVES")
        kingMoveset = set(king.possibleMoves)
        print(kingMoveset)

        print("ENEMY MOVES")
        enemyMoveset = set([move for sub in allPossibleEnemyMoves for move in sub])
        print(enemyMoveset)

        if kingMoveset.issubset(enemyMoveset) and kingMoveset != set():
            return True

    return False    
        
        
def main():
    #setup board
    initBoard()
    #set current player
    currentPlayer = "WHITE"
    #show player board
    drawBoard()

    play = True
    while(play):
            print("CURRENT PLAYER: " + currentPlayer)
            #get move from player
            playerInput = input("Enter move...\n")
            #piece player wants to move
            piece = anToMat(str(playerInput).split(' ')[0])
            #space player wants to move to
            target = anToMat(str(playerInput).split(' ')[1])

            #check if move is acceptable, then switch players
            playerMove = move(board[piece[0]][piece[1]], target, currentPlayer)
            if playerMove:    
                    currentPlayer = "WHITE" if currentPlayer == "BLACK" else "BLACK"
                    updatePieceMoves()

            
            #check if game is in checkmate
            if(determineCheckmate()):
                print("CHECKMATE!")
                play = False
            #play = not determineCheck()
            drawBoard() 

    #determineCheck()
    #determineCheckmate()
    #currentPlayer = not currentPlayer
