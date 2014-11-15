from path_node import *
from heuristic import *
import gameconstants

def alpha_beta(path, depth, isMax, alpha, beta):

	node = path.getTail()
	boardState = node.boardState

	# TODO : depth == 0 || winning state
	if depth == 0 || boardState.isWon():
		return Heuristic.getValue(boardState)

	if isMax:
		for i in range(0, boardState.cols):
			childBoardState = boardState.move(gameconstants.TOP_PLAYER, i)
			if !path.pathContains(childBoardState):
				node.setNext(childBoardState)
				alpha = max(alpha, alpha_beta(path, depth - 1, False, alpha, beta))
				if beta <= alpha:
					break
		return alpha
	else:	# isMin
		for i in range(0, boardState.cols):
			childBoardState = boardState.move(gameconstants.BOTTOM_PLAYER, i)
			if !path.pathContains(childBoardState):
				node.setNext(childBoardState)
				beta = min(beta, alpha_beta(path, depth - 1, True, alpha, beta))
				if beta <= alpha:
					break
		return beta
