#class definition for piece object
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
	if player == "WHITE":
		return "BLACK"
	else:
		return "WHITE"

#calculates possible moves for given piece
def calcAllPositions(piece):
	rank = piece.rank
	position = piece.position

	positionsList = []

	#if piece is a knight, all "L" positions added to list
	if rank == "KNIGHT":
		positionsList.append((position[0] + 1, position[1] + 2))
		positionsList.append((position[0] - 1, position[1] + 2))
		positionsList.append((position[0] + 1, position[1] - 2))
		positionsList.append((position[0] - 1, position[1] - 2))

		positionsList.append((position[0] + 2, position[1] + 1))
		positionsList.append((position[0] - 2, position[1] + 1))
		positionsList.append((position[0] + 2, position[1] - 1))
		positionsList.append((position[0] - 2, position[1] - 1))

	#if piece is a pawn
	elif rank == "PAWN":

		#if there is an enemy diagonally adjacent, can move there
		for side,direction in zip(["WHITE","BLACK"],[-1,1]):
			diagLeft = ( position[0] - 1, position[1] + direction )
			diagRight = ( position[0] + 1, position[1] + direction)

			#for each space diagonally up left, right
			for square in [diagLeft,diagRight]:
				#if space is not out of bounds
				if not outOfBounds(square):
					adjacentPiece = board[square[0]][square[1]]

					#if space contains an enemy piece, add to list
					if adjacentPiece.player == enemySide(piece.player):
						positionsList.append(square)

			#default movement is forward 1 and forward 2 spaces
			positionsList.append((position[0] , position[1] + direction))
			positionsList.append((position[0] , position[1] + direction*2))

	#if piece is a king
	elif rank == "kING":
		topleft = ( position[0]  - 1, position[1] - 1 )
		botright = ( position[0]  + 1, position[1] + 1 )

		for i in range(topleft[0], botright[0]):
			for j in range(topleft[1], botright[1]):
				if (i,j) == position or board[i][j].player == piece.player or outOfBounds( (i,j) ):
					continue
				print((i,j))
				positionsList.append( (i,j) )

	#if piece is a queen
	elif rank == "QUEEN":
		#queen can move any direction, limitless

		square = position
		#up
		while(not outOfBounds(square) ):
			square = ( square[0] , square[1] - 1)
			positionsList.append( (square[0], square[1]) )

		square = position
		#down
		while(not outOfBounds(square) ):
			square = ( square[0] , square[1] + 1)
			positionsList.append( (square[0], square[1]) )

		square = position
		#left
		while(not outOfBounds(square) ):
			square = ( square[0]  - 1, square[1] )
			positionsList.append( (square[0], square[1]) )
		
		square = position
		#right
		while(not outOfBounds(square) ):
			square = ( square[0]  + 1, square[1] )
			positionsList.append( (square[0], square[1]) )

		square = position
		#upRight
		while(not outOfBounds(square) ):
			square = ( square[0]  + 1, square[1] - 1)
			positionsList.append( (square[0], square[1]) )

		square = position
		#upLeft
		while(not outOfBounds(square) ):
			square = ( square[0]  - 1, square[1] - 1)
			positionsList.append( (square[0], square[1]) )

		square = position
		#downRight
		while(not outOfBounds(square) ):
			square = ( square[0]  + 1, square[1] + 1)
			positionsList.append( (square[0], square[1]) )

		square = position
		#downLeft
		while(not outOfBounds(square) ):
			square = ( square[0]  - 1, square[1] + 1)
			positionsList.append( (square[0], square[1]) )

	#if piece is a rook
	elif rank == "ROOK":

		square = position
		#up
		while(not outOfBounds(square) ):
			square = ( square[0] , square[1] - 1)
			positionsList.append( (square[0], square[1]) )

		square = position
		#down
		while(not outOfBounds(square) ):
			square = ( square[0] , square[1] + 1)
			positionsList.append( (square[0], square[1]) )

		square = position
		#left
		while(not outOfBounds(square) ):
			square = ( square[0]  - 1, square[1] )
			positionsList.append( (square[0], square[1]) )
		
		square = position
		#right
		while(not outOfBounds(square) ):
			square = ( square[0]  + 1, square[1] )
			positionsList.append( (square[0], square[1]) )

	#if piece is a bishop
	elif rank == "BISHOP":

		square = position
		#upRight
		while(not outOfBounds(square) ):
			square = ( square[0]  + 1, square[1] - 1)
			positionsList.append( (square[0], square[1]) )

		square = position
		#upLeft
		while(not outOfBounds(square) ):
			square = ( square[0]  - 1, square[1] - 1)
			positionsList.append( (square[0], square[1]) )

		square = position
		#downRight
		while(not outOfBounds(square) ):
			square = ( square[0]  + 1, square[1] + 1)
			positionsList.append( (square[0], square[1]) )

		square = position
		#downLeft
		while(not outOfBounds(square) ):
			square = ( square[0]  - 1, square[1] + 1)
			positionsList.append( (square[0], square[1]) )
		

	#remove any out of bounds positions
	positionsList = list(filter(lambda tup: (tup[0] < 8 and tup[0] >= 0) 
										and (tup[1] < 8 and tup[1] >= 0),positionsList))

	invalidPosList = []

	#remove positions with pieces on board of same side
	for pos in positionsList:
		if board[pos[0]][pos[1]].player == piece.player:
			invalidPosList.append(pos)

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
def determineCheck():
	for side in ["WHITE","BLACK"]:
		if side == "WHITE":
			king = list(filter( (lambda p : p.rank == "kING"), whiteSide))[0]
			for piece in blackSide:
				if king.position in piece.possibleMoves:
					return True
				else:
					return False

		if side == "BLACK":
			king = list(filter( (lambda p : p.rank == "kING") ,blackSide))[0]
			for piece in whiteSide:
				if king.position in piece.possibleMoves:
					return True
				else:
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

main()	
