#!/usr/bin/python

from player import Player
from heuristic import Heuristic
import gameconstants
import ui
import time

class And_Or_Player(Player):

    def __init__(self, player):
        Player.__init__(self, player_num=player)


    def move(self, board): 
        start_time = time.time()
        bestMove = self.orMove(board, 1)
        end_time = time.time()
        log = (str(board.getCols()) + ", " + str(gameconstants.numPlys) 
            + ", " + str(end_time - start_time) + "\n")
        # w for writing
        with open("and_or_times.txt", "a") as andOrFile:
            andOrFile.write(log)

        return bestMove[0]

    # And is for the oppenent
    def andMove(self, board, depth):

    	# find the possible moves
    	possMoves = []
    	for i in range(0, board.getCols()):
    		curBin = board.getBin(self.player, (i+1))
    		if curBin != 0:
    			possMoves.append(i)

    	# generate all possible board states
    	possBoardStates = []
    	for i in possMoves:
    		possBoardStates.append(board.move(self.player, (i+1)))

    	# check to see if end
        hVals = []
    	if depth >= gameconstants.numPlys:
    		# if so return the worst, since we are assuming the oppent
    		# will play as well as possible
    		# get heuristic values
	    	for i in possBoardStates:
	    		hVals.append(Heuristic.getValue(i, self.player))
        else:
    		depth = depth + 1
    		# get the hVals
                for b in possBoardStates:
                        m,h=self.orMove(b, depth)
                        hVals.append(h)

        # determine the worst (for the AI player)
        worst = hVals[0];
        for h in hVals:
            if h < worst: worst = h

        return worst

    # Or is for the AI
    def orMove(self, board, depth):

    	# find the possible moves
    	possMoves = []
    	# index for get bin starts at 1
    	for i in range(1, board.getCols()+1):
    		curBin = board.getBin(self.player, (i))
    		#ui.UI.debug("bin @ " + str(i) + " has " + str(curBin))
    		if curBin != 0:
    			possMoves.append(i)

    	ui.UI.debug("possible moves : " + str(possMoves))

    	# generate all possible board states
    	possBoardStates = []
    	for i in possMoves:
    		possBoardStates.append(board.move(self.player, (i)))

    	# check if the end
        hVals = []
    	if depth >= gameconstants.numPlys:
            # get heuristic values
            for b in possBoardStates:
                    hVals.append(Heuristic.getValue(b, self.player))
   	else:
            depth = depth + 1
            for b in possBoardStates:
                hVals.append(self.andMove(b, depth))

        # determine the best
        if (len(hVals) > 0):
            best = hVals[0]
            bestMoveIndex = 0
            for i in range(1, len(hVals)):
                    if hVals[i] > best:
                            best = hVals[i]
                            bestMoveIndex = i

        bestMove = possMoves[bestMoveIndex]
        return (bestMove, hVals[bestMoveIndex])
 
    def __str__(self):
        return "And-Or Algorithm"

    @staticmethod
    def isComputer(): return True

    @staticmethod
    def optName(): return "andor"
