#!/usr/bin/python

from player import Player

class Human_Player(Player):

    def __init__(self, player, ui):
        Player.__init__(self, player_num=player)
        self.ui = ui

    def move(self, board):
        return self.ui.interact(self.player, board)

    def __str__(self):
        return "Human Player"

    def isComputer(self):
        return False

