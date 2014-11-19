#!/usr/bin/python

import gameconstants


class Human_Player(Player):

    def __init__(self, player, ui):
        super(Alpha_Beta_Player, self,).init(player_num=player)
        self.ui = ui

    def move(self, board):
        return self.ui.interact(self.player)



