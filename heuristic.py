from board import *

class Heuristic:

	def __init__ (self, length):
		self.tableLen = length


		# calculate the constant values ahead of time
		self.constants = []
		for i in range(0, length):
			self.constants.append(i+1)

	def getValue (self, board):
		p1Bins = board.p1
		p2Bins = board.p2

		p1Sum = 0
		p2Sum = 0

		for i in range(0, self.tableLen):
			p1Sum = p1Sum + (p1Bins[i] * self.constants[i])
			p2Sum = p2Sum + (p2Bins[self.tableLen - (i + 1)] 
				* self.constants[self.tableLen - (i + 1)])

		return p1Sum - p2Sum


if __name__ == "__main__":
	board = Board(10, 4)
	h = Heuristic(10)
	print h.getValue(board)