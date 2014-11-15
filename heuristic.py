from board import *
from gameconstants import *

class Heuristic:

	def __init__ (self, length):
		self.tableLen = length


		# calculate the constant values ahead of time
		self.constants = []
		for i in range(0, length):
			self.constants.append(length - i)

	def getValue (self, board):
		p1Bins = board.p1
		p2Bins = board.p2

		p1Sum = 0
		p2Sum = 0

		for i in range(0, self.tableLen):
			p1Sum = p1Sum + (p1Bins[i] * self.constants[i])
			p2Sum = p2Sum + (p2Bins[i] * self.constants[i])

		print "p1Sum:"
		print  p1Sum
		print "p2Sum:"
		print  p2Sum

		return p1Sum - p2Sum


if __name__ == "__main__":
	board = Board(4, 4)
	h = Heuristic(4)
	print h.getValue(board)
	newBoard = board.move(TOP_PLAYER, 1)
	print h.getValue(newBoard)