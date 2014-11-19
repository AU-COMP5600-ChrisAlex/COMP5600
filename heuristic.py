#!/usr/bin/python

from board import *
import gameconstants 
import ui

class Heuristic:

        _constants = []
        _constants_valid = False


        @staticmethod
        def _makeConstants():
            for i in range(0, gameconstants.numRows):
                Heuristic._constants.append(gameconstants.numRows - i)

        @staticmethod
	def getValue(board, player):

            if not Heuristic._constants_valid:
                Heuristic._makeConstants()

            if player == gameconstants.TOP_PLAYER:    
                p1Bins = board.p1
                p2Bins = board.p2
            elif player == gameconstants.BOTTOM_PLAYER:    
                p1Bins = board.p2
                p2Bins = board.p1
            else:
                raise ValueError("Invalid Player")

	    p1Sum = 0
	    p2Sum = 0

	    for i in range(0, gameconstants.numRows):
		    p1Sum = p1Sum + (p1Bins[i] * Heuristic._constants[i])
		    p2Sum = p2Sum + (p2Bins[i] * Heuristic._constants[i])

            UI.debug("p1Sum: " + str(p1Sum))
            UI.debug("p2Sum: " + str(p2Sum))

	    return p1Sum - p2Sum


if __name__ == "__main__":
        gameconstants.numRows = 4
        gameconstants.numPebbles=4
	board = Board()
	UI.debug(Heuristic.getValue(board, gameconstants.TOP_PLAYER))
	newBoard = board.move(gameconstants.TOP_PLAYER, 1)
	UI.debug(Heuristic.getValue(newBoard, gameconstants.TOP_PLAYER))
