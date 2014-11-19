#!/usr/bin/python

from path_node import *
from heuristic import *
import gameconstants
from player import Player
from operator import itemgetter
from sys import maxint



class Alpha_Beta_Player(Player):

    def __init__(self, player):
        Player.__init__(self, player_num=player)
        #super(Alpha_Beta_Player, self).__init__(player_num=num)

    
    #returns integer representing which bin to move
    def move(self, board):

        alpha = -maxint-1
        beta = maxint
        v = -maxint-1
        a = None

        #TODO: we should instantiate path here, and check 
        #to see if b in path in the for loop as well

        for m, h in self._order_moves(board):

            b = board.move(self.player,m)
            path = PathNode(board)

            v_prime= self._alpha_beta(path, gameconstants.numPlys, False, alpha, beta)

            if v_prime > v: 
                v = v_prime
                a = m
            if v >= beta: return a
            elif v > alpha: a = v

        return a

    def _order_moves(self, board):
        moves = []
        for i in range(1, len(board) + 1):
            if board.getBin(self.player, i) != 0:
                moves.append((i,Heuristic.getValue(board.move(self.player, i), self.player)))

        return sorted(moves,key=itemgetter(1))


    def _alpha_beta(self, path, depth, isMax, alpha, beta):

            node = path.getTail()
            boardState = node.boardState

            # TODO : depth == 0 || winning state
            if depth == 0 or boardState.isWon():
                    return Heuristic.getValue(boardState, self.player)

            if isMax:
                    for i in range(0, boardState.cols):
                            childBoardState = boardState.move(gameconstants.TOP_PLAYER, i)
                            if not path.pathContains(childBoardState):
                                    node.setNext(childBoardState)
                                    alpha = max(alpha, self._alpha_beta(path, depth - 1, False, alpha, beta))
                                    if beta <= alpha:
                                            break
                    return alpha
            else:	# isMin
                    for i in range(0, boardState.cols):
                            childBoardState = boardState.move(gameconstants.BOTTOM_PLAYER, i)
                            if not path.pathContains(childBoardState):
                                    node.setNext(childBoardState)
                                    beta = min(beta, self._alpha_beta(path, depth - 1, True, alpha, beta))
                                    if beta <= alpha:
                                            break
                    return beta



