class Piece:
	def __init__(self, rank, player, position, possibleMoves):
		self.rank = rank
		self.player = player
		self.position = position
		self.possibleMoves = possibleMoves


whiteSide = []
blackSide = []

board = []
for i in range(8):
	row = []
	for j in range(8):
		row.append(Piece("EMPTY","NONE",(i,j),[]))
	board.append(row)

def outOfBounds(position):
	if (position[0] >= 0 and position[0] <= 7) and (position[1] >= 0 and position[1] <= 7):
		return False
	return True

def enemySide(player):
	if player == "WHITE":
		return "BLACK"
	else:
		return "WHITE"

def calcAllPositions(piece):
	rank = piece.rank
	position = piece.position

	positionsList = []

	if rank == "KNIGHT":
		positionsList.append((position[0] + 1, position[1] + 2))
		positionsList.append((position[0] - 1, position[1] + 2))
		positionsList.append((position[0] + 1, position[1] - 2))
		positionsList.append((position[0] - 1, position[1] - 2))

		positionsList.append((position[0] + 2, position[1] + 1))
		positionsList.append((position[0] - 2, position[1] + 1))
		positionsList.append((position[0] + 2, position[1] - 1))
		positionsList.append((position[0] - 2, position[1] - 1))

	elif rank == "PAWN":
		for side,direction in zip(["WHITE","BLACK"],[-1,1]):
			diagLeft = ( position[0] - 1, position[1] + direction )
			diagRight = ( position[0] + 1, position[1] + direction)

			for square in [diagLeft,diagRight]:
				if not outOfBounds(square):
					adjacentPiece = board[square[0]][square[1]]

					if adjacentPiece.player == enemySide(piece.player):
						positionsList.append(square)

			positionsList.append((position[0] , position[1] + direction))
			positionsList.append((position[0] , position[1] + direction*2))

	#remove any out of bounds positions
	positionsList = list(filter(lambda tup: (tup[0] < 8 and tup[0] >= 0) 
										and (tup[1] < 8 and tup[1] >= 0),positionsList))

	invalidPosList = []

	for pos in positionsList:
		if board[pos[0]][pos[1]].player == piece.player:
			invalidPosList.append(pos)

	positionsList = list(set(positionsList) - set(invalidPosList))

	return positionsList
	

def validMove(piece, target, player):
	correctPlayer = piece.player == player
	possiblePositions = calcAllPositions(piece)
	if correctPlayer and (target in possiblePositions):
		return True
	else:
		return False

def move(piece, target, player):
	print(piece.possibleMoves)
	if validMove(piece, target, player):
		board[piece.position[0]][piece.position[1]] = Piece("EMPTY","NONE",piece.position,[])
		piece.position = target
		board[target[0]][target[1]] = piece
		print(player + " MOVES " + piece.rank + " TO " + str(target))
		return True
	else:
		print("INVALID MOVE")
		return False

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
		board[3][i] = Piece("kING",side,(3,i),[])		
		board[4][i] = Piece("QUEEN",side,(4,i),[])		

		if side == "WHITE":
			whiteSide.append(board[3][i])
			whiteSide.append(board[4][i])

		if side == "BLACK":
			blackSide.append(board[3][i])
			blackSide.append(board[4][i])

	for i in range(8):
		for j in range(8):
				board[i][j].possibleMoves = calcAllPositions(board[i][j])

alphabet = "ABCDEFGH"
coordDict = {alphabet[i] : i for i in list(range(8))}

def anToMat(coords):
	xcoord = int(coordDict[coords[0]])
	ycoord = 8 - int(coords[1])

	return (xcoord,ycoord)

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

def main():
	initBoard()
	currentPlayer = "WHITE"
	drawBoard()

	play = True
	while(play):
			print("CURRENT PLAYER: " + currentPlayer)
			playerInput = input("Enter move...\n")
			piece = anToMat(str(playerInput).split(' ')[0])
			target = anToMat(str(playerInput).split(' ')[1])

			playerMove = move(board[piece[0]][piece[1]], target, currentPlayer)
			if playerMove:	
					currentPlayer = "WHITE" if currentPlayer == "BLACK" else "BLACK"

			play = not determineCheck()
			drawBoard() 

	#determineCheck()
	#determineCheckmate()
	#currentPlayer = not currentPlayer

main()	
