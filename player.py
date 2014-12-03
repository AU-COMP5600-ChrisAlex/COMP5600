#!/usr/bin/python

import gameconstants


#ABSTRACT CLASS that defines a 'move' method returning which bin the player wants to move
class Player:

    def __init__(self, player_num):
        if player_num == gameconstants.TOP_PLAYER:
            self.player = gameconstants.TOP_PLAYER
        elif player_num == gameconstants.BOTTOM_PLAYER:
            self.player = gameconstants.BOTTOM_PLAYER
        else:
            raise ValueError("Invalid Player Number")

    #return bin to move
    def move(self):
        raise RuntimeError("THIS IS A VIRTUAL METHOD, USE A DERIVED CLASS")

    #return the algorithm in use
    def __str__(self):
        raise RuntimeError("THIS IS A VIRTUAL METHOD, USE A DERIVED CLASS")



