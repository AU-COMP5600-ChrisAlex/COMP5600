from board import *
from gameconstants import *

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
	board = Board(10, 4)
	head = PathNode(board)

	print head.getTail().getBoardState().getBin(TOP_PLAYER, 1)

	board2 = Board(10, 5)
	head.setNext(board2)

	print head.getTail().getBoardState().getBin(TOP_PLAYER, 1)	