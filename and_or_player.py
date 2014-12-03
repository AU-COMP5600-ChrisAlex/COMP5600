#!/usr/bin/python

from player import Player

class And_Or_Player(Player):

    def __init__(self, player):
        Player.__init__(self, player_num=player)


    def move(self, board):
        raise NotImplementedError("And-Or player not implemented")

    def __str__(self):
        return "And-Or Algorithm"

    def isComputer(self): return True
