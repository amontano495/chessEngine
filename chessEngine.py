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

#calculate list of valid moves pawn piece can make
def pawnPositions(color, position, board):
    positionsList = []

    #black pieces move down the board, white pieces move up
    direction = 1 if color == "black" else -1


    #if there is no enemy directly in front
    if board[position[0]][position[1] + direction] == None:
        #pawn is able to move forward
        moveForward = (position[0], position[1] + direction)
        positionsList.append(moveForward)

    #pawn can move diagonally if enemy present
    diagLeft = (position[0] - 1, position[1] + direction)
    diagRight = (position[0] + 1, position[1] + direction)

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

#calculate list of valid moves Knight piece can make
def knightPositions(position):
    positionsList = []

    #Knight can only move in L shape patterns
    positionsList.append((position[0] + 1, position[1] + 2))
    positionsList.append((position[0] - 1, position[1] + 2))
    positionsList.append((position[0] + 1, position[1] - 2))
    positionsList.append((position[0] - 1, position[1] - 2))
    
    positionsList.append((position[0] + 2, position[1] + 1))
    positionsList.append((position[0] - 2, position[1] + 1))
    positionsList.append((position[0] + 2, position[1] - 1))
    positionsList.append((position[0] - 2, position[1] - 1))
            
    return positionsList


#calculate list of valid moves Bishop piece can make
def bishopPositions(position, board):
    positionsList = []

    #bishop makes unlimited diagonal moves

    #starting positions first
    upLeft = position
    upRight = position
    downLeft = position
    downRight = position

    #we will construct diagonal paths
    upLeftPath = []
    upRightPath = []
    downLeftPath = []
    downRightPath = []

    #add tiles to paths, longest possible path length is 8
    for i in range(8):
        upLeft = (upLeft[0] - 1, upLeft[1] - 1)
        upLeftPath.append(upLeft)

        upRight = (upRight[0] + 1, upRight[1] - 1)
        upRightPath.append(upRight)

        downLeft = (downLeft[0] - 1, downLeft[1] + 1)
        downLeftPath.append(downLeft)

        downRight = (downRight[0] + 1, downRight[1] + 1)
        downRightPath.append(downRight)

    #paths must be constrained obstructing pieces
    upLeftPath = rookHelper(upLeftPath, board)
    upRightPath = rookHelper(upRightPath, board)
    downLeftPath = rookHelper(downLeftPath, board)
    downRightPath = rookHelper(downRightPath, board)

    #final list is sum of the paths
    positionsList = upLeftPath + upRightPath + downLeftPath + downRightPath

    return positionsList

#constrains piece movesets with obstructing pieces
def rookHelper(pathList, board):
    count = 0
    newPath = pathList

    for pos in pathList:
        count += 1
        (x,y) = pos
        if not outOfBounds(pos):
            #if there is an obstructing piece (any color)
            if board[x][y] != None:
                #cut off the path at that point
                newPath = pathList[:count]
                break

    return newPath

#calculate list of valid moves Rook piece can make
def rookPositions(position, board):
    positionsList = []

    #rook can make unlimited side-to-side, up & down moves
    horizontal = []
    vertical = []

    #create horizontal, vertical paths
    x,y = position
    for i in range(8):
        if (i,y) != position:
            horizontal.append( (i,y) )
        if (x,i) != position:
            vertical.append( (x,i) )

    #separate vertical path into up and down
    upPath = []
    downPath = []
    for tile in vertical:
        if tile[1] < y:
            upPath.append(tile)
        elif tile[1] > y:
            downPath.append(tile)

    #up path is actually backwards since we startd counting from the bottom
    upPath.reverse()

    #separate horizontal path into left and right
    leftPath = []
    rightPath = []    
    for tile in horizontal:
        if tile[0] < x:
            leftPath.append(tile)
        elif tile[0] > x:
            rightPath.append(tile)

    #similar issue with up path
    leftPath.reverse()

    #constrain paths with regards to obstructing pieces
    #the order of the path is important here, hence the reversing
    upPath = rookHelper(upPath, board)
    downPath = rookHelper(downPath, board)
    leftPath = rookHelper(leftPath, board)
    rightPath = rookHelper(rightPath, board)

    #final list of moves is sum of constructed paths
    positionsList = leftPath + rightPath + upPath + downPath

    return positionsList

#calculate list of valid moves Queen piece can make
def queenPositions(rank, color, position, board, players):

    #very simple to calculate, just combine rook and bishop moves
    orthogonalMoves = rookPositions(position, board)
    diagonalMoves = bishopPositions(position, board)

    positionsList = orthogonalMoves + diagonalMoves
    
    return positionsList

#calculate list of valid moves King piece can make
def kingPositions(rank, color, position, board, players):
    positionsList = []

    #king cannot move into tiles under attack by enemy
    if color == "white":
        possibleEnemyPositions = players[1].possibleNextMoves
    else:
        possibleEnemyPositions = players[0].possibleNextMoves

    #king can move around in a 3x3 square
    #start by setting top left and bottom right squares
    topleft = ( position[0]  - 1, position[1] - 1 )
    botright = ( position[0]  + 1, position[1] + 1 )

    #traverse through each tile in 3x3 square
    for i in range(topleft[0], botright[0] + 1):
        for j in range(topleft[1], botright[1] + 1):
            #tile must not be the position the king is in, out of bounds or in enemy attack
            if (i,j) != position and not outOfBounds((i,j)) and (i,j) not in possibleEnemyPositions:
                positionsList.append( (i,j) )

    return positionsList


#calculates possible moves for given piece
def calcAllPositions(rank, color, position, board, players):
    positionsList = []

    #if piece is a knight, all "L" positions added to list
    if rank == "knight":
        positionsList = knightPositions(position)

    #if piece is a pawn
    elif rank == "pawn":
        positionsList = pawnPositions(color, position, board)

    #if piece is a king
    elif rank == "king":
        positionsList = kingPositions(rank, color, position, board, players)

    #if piece is a queen
    elif rank == "queen":
        positionsList = queenPositions(rank, color, position, board, players)

    #if piece is a rook
    elif rank == "rook":
        positionsList = rookPositions(position, board)

    #if piece is a bishop
    elif rank == "bishop":
        positionsList = bishopPositions(position, board)

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

    #for extra measure, remove any invalid moves from the final list
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
def determineCheckmate(player, enemy_player, board):
    #first, find the king piece
    for piece in player.pieces:
        if piece.rank == "king":
            king = piece

    #we will examine tiles around king
    surroundingTiles = []
    position = king.board_pos

    topleft = ( position[0]  - 1, position[1] - 1 )
    botright = ( position[0]  + 1, position[1] + 1 )

    #tiles under attack by enemy
    possibleEnemyPositions = enemy_player.possibleNextMoves

    #grab all the neighboring tiles into a list
    neighbors = []
    for i in range(topleft[0], botright[0] + 1):
        for j in range(topleft[1], botright[1] + 1):
            if not outOfBounds( (i,j) ) and (i,j) != king.board_pos:
                neighbors.append( (i,j) )

    #look if all neighbors are friendly pieces or if a safe spot exists
    #a "safe spot" is a position that is open and not under attack
    safeTileExists = False
    friendlyNeighbors = 0
    for tile in neighbors:
        x,y = tile
        #if position on the board has no piece and not under attack
        if board[x][y] == None and tile not in possibleEnemyPositions:
            safeTileExists = True
        if board[x][y] != None:
            #if position on board is friendly
            if board[x][y].color == king.color:
                friendlyNeighbors += 1
    #if there is a safe spot or all the neighbors are friendly 
    if safeTileExists or friendlyNeighbors == len(neighbors):
        #then player has not been checkmated
        return False

    return True
