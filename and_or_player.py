#!/usr/bin/python

import gameconstants

class And_Or_Player(Player):

    def __init__(self, player):
        super(Alpha_Beta_Player, self,).init(player_num=player)


    def move(self, board):
        raise NotImplementedError("And-Or player not implemented")
