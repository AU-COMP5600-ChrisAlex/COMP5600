#!/usr/bin/python

from player import Player
from heuristic import Heuristic

class And_Or_Player(Player):

    def __init__(self, player):
        Player.__init__(self, player_num=player)


    def move(self, board):
        bestMove = orMove(board, 1)
        return bestMove[0]

    # And is for the oppenent
    def andMove(self, board, depth):

    	# find the possible moves
    	possMoves = []
    	for i in range(0, board.getCols()):
    		curBin = board.getBin(self, (i+1))
    		if curBin != 0:
    			possMoves.append(i)

    	# generate all possible board states
    	possBoardStates = []
    	for i in range(0, len(possMoves)):
    		possBoardStates.append(board.move(self, (i+1)))

    	# check to see if end
    	if depth == gameconstants.numPlys:

    		# if so return the worst, since we are assuming the oppent
    		# will play as well as possible
    		# get heuristic values
	    	hVals = []
	    	for i in range(0, len(possBoardStates)):
	    		hVals.append(Heuristic.getValue(possBoardStates[i], self))

	    	# determine the worst (for the AI player)
	    	worst = hVals[0];
	    	worstMoveIndex = 0
	    	for i in range(1, len(hVals)):
	    		if hVals[i] < worst:
	    			worst = hVals[i]
	    			worstMoveIndex = i

	    	worstMove = possMoves[worstMoveIndex]
    		return (worstMove, hVals[worstMoveIndex])
    	else:
    		depth = depth + 1

    		# get the responses
    		responses = []
    		for i in range(0, len(possMoves)):
    			responses.append(orMove(board, depth))

    		# find the worst
    		worst = responses[0][1]
    		worstMoveIndex = 0
    		for i in range(0, len(responses)):
    			if responses[i][1] < worst:
    				worst = responses[i][1]
    				worstMoveIndex = i

    		worstMove = possMoves[worstMoveIndex]
    		return (worstMove, responses[worstMoveIndex][1])


    # Or is for the AI
    def orMove(self, board, depth):

    	# find the possible moves
    	possMoves = []
    	for i in range(0, board.getCols()):
    		curBin = board.getBin(self, (i+1))
    		if curBin != 0:
    			possMoves.append(i)

    	# generate all possible board states
    	possBoardStates = []
    	for i in range(0, len(possMoves)):
    		possBoardStates.append(board.move(self, (i+1)))

    	# get heuristic values
    	hVals = []
    	for i in range(0, len(possBoardStates)):
    		hVals.append(Heuristic.getValue(possBoardStates[i], self))

    	# determine the best
    	best = hVals[0];
    	bestMoveIndex = 0
    	for i in range(1, len(hVals)):
    		if hVals[i] > best:
    			best = hVals[i]
    			betsMoveIndex = i

    	# check if the end
    	if depth == gameconstants.numPlys:
    		bestMove = possMoves[bestMoveIndex]
    		return (bestMove, hVals[bestMoveIndex])
    	else:
    		depth = depth + 1
    		return orMove(possBoardStates[bestMoveIndex], depth)

    def __str__(self):
        return "And-Or Algorithm"

    def isComputer(self): return True
