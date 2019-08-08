class Piece:
	def __init__(self, rank, player, position, possibleMoves):
		self.rank = rank
		self.player = player
		self.position = position
		self.possibleMoves = possibleMoves

board = []
for i in range(8):
	row = []
	for j in range(8):
		row.append(Piece("EMPTY","NONE",(i,j),[]))
	board.append(row)

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

	#remove any out of bounds positions
	positionsList = list(filter(lambda tup: tup[0] >= 0 and tup[1] >= 0,positionsList))

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
	if validMove(piece, target, player):
		board[piece.position[0]][piece.position[1]] = Piece("EMPTY","NONE",piece.position,[])
		piece.position = target
		board[target[0]][target[1]] = piece
		print(player + " MOVES " + piece.rank + " TO " + str(target))
	else:
		print("INVALID MOVE")
		return

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

testPiece = Piece("KNIGHT","WHITE",(3,3),[])
board[3][3] = testPiece

testPiece = Piece("KNIGHT","BLACK",(4,5),[])
board[4][5] = testPiece

board[3][3].possibleMoves = calcAllPositions(board[3][3])
board[4][5].possibleMoves = calcAllPositions(board[4][5])

alphabet = "ABCDEFGH"
coordDict = {alphabet[i] : i for i in list(range(8))}

def anToMat(coords):
	xcoord = int(coordDict[coords[0]])
	ycoord = 8 - int(coords[1])

	return (xcoord,ycoord)


def main():
	currentPlayer = "WHITE"
	drawBoard()
	while(True):
			playerInput = input("Enter move...\n")
			piece = anToMat(str(playerInput).split(' ')[0])
			target = anToMat(str(playerInput).split(' ')[1])
			move(board[piece[0]][piece[1]], target, "WHITE")
			drawBoard()

	#move(piece, target, currentPlayer)
	#determineCheck()
	#determineCheckmate()
	#currentPlayer = not currentPlayer

main()	
