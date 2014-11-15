from board import *

class Heuristic:

	def __init__ (self, length):
		self.tableLen = length

		# calculate the constant values ahead of time
		for i in range(0, self.length):
			self.constants[i] = i+1

	def getValue (board):
		p1Bins = board.p1
		p2Bins = reversed(board.p2)

		p1Sum = 0
		p2Sum = 0

		for i in range(0, self.length):

			p1Sum = p1Sum + (p1Bins[i] * self.constants[i])
			p2Sum = p2Sum + (p2Bins[i] * self.constants[i])

		return p1Sum - p2Sum
