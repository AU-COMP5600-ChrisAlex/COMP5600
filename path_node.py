from board import *
import gameconstants 

class PathNode:

	def __init__(self, boardState):
		self.boardState = boardState
		self.next = None
		self.isTail = True

	def setNext(self, boardState):
		self.next = PathNode(boardState)
		self.isTail = False

	def getNext(self):
		return self.next

	def getTail(self):
		if self.isTail:
			return self
		else:
			return self.next.getTail()

	def getBoardState(self):
		return self.boardState

	def pathContains(self, boardState):
		if self.boardState.isEquivalent(boardState):
			return True
		elif self.isTail and not(self.boardState.isEquivalent(boardState)):
			return False
		else:
			return self.next.pathContains(boardState)

if __name__ == "__main__":
        gameconstants.numRows = 10
        gameconstants.numPebbles = 4
	board = Board()
	head = PathNode(board)

	print head.getTail().getBoardState().getBin(gameconstants.TOP_PLAYER, 1)

        gameconstants.numPebbles = 5
	board2 = Board()
	head.setNext(board2)

	print head.getTail().getBoardState().getBin(gameconstants.TOP_PLAYER, 1)	
