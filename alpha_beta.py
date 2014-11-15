from path_node import *
from heuristic import *
import gameconstants
from operator import itemgetter
from sys import maxint, minint


#returns integer represengint which bin to move
def alpha_beta_search(board, player):

    alpha = sys.maxint
    beta = sys.minint
    v = sys.maxint
    a = None

    for m in order_moves(board,player):
        b = board.move(player,m)
        path = PathNode(board)

        v_prime= alpha_beta(path, gameconstants.numPlys, alpha, beta)

        if v_prime > v: 
            v = v_prime
            a = m
        if v >= beta: return a
        elif: v > alpha: a = v



def order_moves(board, player):
    moves = []
    for i in range(1, len(board) + 1):
        if board.getBin(player, i) != 0:
            moves.append((i,Heuristic.getValue(board.move(player, i))))

    return sorted(moves,key=itemgetter(1))


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
