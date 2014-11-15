class PathNode:

	def __init__(self, boardState):
		self.boardState = boardState
		self.next = None
		self.isHead = True
		self.isTail = True

	def setNext(self, boardState):
		self.next = PathNode(boardState)
		self.isTail = False
		self.next.isHead = False

	def getNext(self):
		return self.next

	def getTail(self):
		if (self.isTail):
			return self
		else:
			return self.next.getTail()

	def pathContains(self, boardState):
		if self.boardState.isEquivalent(boardState):
			return True
		elif self.isTail && !self.boardState.isEquivalent(boardState):
			return False
		else:
			return self.next.pathContains(boardState)