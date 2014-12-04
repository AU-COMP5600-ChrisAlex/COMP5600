#!/usr/bin/python


import array
from ui import UI
import gameconstants 


class Board:

    def __len__(self):
        return self.cols

    def __init__(self, player1=None, player2=None):

        self.cols=gameconstants.numRows
        self.startPebs = gameconstants.numPebbles

        if player1==None and player2==None:
            self.p1=array.array("I",(self.startPebs,)*self.cols)
            #self.p1=array.array("I",range(1,self.cols+1))

            self.p2=array.array("I")
            self.p2.extend(self.p1)
        else:
            self.p1 = array.array("I",(0,)*self.cols)
            self.p2=array.array("I")
            self.p2.extend(self.p1)
            
            #copy values by value
            for i in range(0, self.cols):
                self.p1[i] = player1[i]
                self.p2[i] = player2[i]
            
    def getCols(self):
        return self.cols


    def move(self,player,bin):  


        movefrom = None
        moveto = None
        bin = bin -1; #array is 0-index, but paramater is not

        if bin < 0 or bin >= self.cols:
            raise IndexError("Invalid Bin: " + str(bin) + " With board state:\n" + str(self))

        if self.getBin(player,bin+1) == 0:
            raise RuntimeError("Illegal Move - Bin contains 0 pebbles")

        # create new board state
        newBoardState = Board(self.p1, self.p2)

        # determine which player
        if player == gameconstants.TOP_PLAYER:
            movefrom = newBoardState.getPlayer(gameconstants.TOP_PLAYER)
            moveto   = newBoardState.getPlayer(gameconstants.BOTTOM_PLAYER)
        elif player == gameconstants.BOTTOM_PLAYER:
            movefrom = newBoardState.getPlayer(gameconstants.BOTTOM_PLAYER)
            moveto   = newBoardState.getPlayer(gameconstants.TOP_PLAYER)
        else:
            raise ValueError("Invalid Player")

        pebbles = movefrom[bin] #pick up the pebbles
        movefrom[bin] = 0       #empty the bin we picked up
        bin += 1                #start at the next bin

        while pebbles > 0:
            while bin < self.cols and pebbles > 0:
                movefrom[bin]+=1
                pebbles -= 1
                bin += 1

            bin = 0

            while bin < self.cols and pebbles > 0:
                moveto[bin]+=1
                pebbles -= 1
                bin += 1

            bin = 0

        return newBoardState

    #bin is indexed from [1,self.cols]
    def getBin(self,player,bin):
        if bin-1 < 0 or bin > self.cols:
            raise IndexError("Invalid Bin: " + str(bin) + " With board state:\n" + str(self))

        if player == gameconstants.TOP_PLAYER:
            return self.p1[bin-1]
        elif player == gameconstants.BOTTOM_PLAYER:
            return self.p2[bin-1]
        else:
            raise ValueError("Invalid Player")

    def isEquivalent(self, boardState):
        if boardState.p1 == self.p1:
            if boardState.p2 == self.p2:
                return True
        return False

    def isWon(self):
        return (self.whoWon() != -1)

    #TODO: MAKE FASTER WITH NUMPY
    def whoWon(self):
        if sum(self.p1) == 0: return gameconstants.TOP_PLAYER
        elif sum(self.p2) == 0: return gameconstants.BOTTOM_PLAYER
        else: return -1

    def getPlayer(self, player):
        if player == gameconstants.TOP_PLAYER:
            return self.p1
        elif player == gameconstants.BOTTOM_PLAYER:
            return self.p2
        else:
            raise ValueError("Invalid Player")
        
    def toString(self):
        
        s1 = "|"
        s2 = "|"

        for i in self.p1.tolist():
            s1 += '{:^4n}|'.format(i)

        #does not actually reverese list, just provides a reverse iterator
        for i in reversed(self.p2.tolist()): 
            s2 += '{:^4n}|'.format(i)

        return s1 + "\n|" + "-" * ( (5*len(self.p1)) - 1 ) + "|\n" + s2

    def __str__(self):
        return self.toString()



