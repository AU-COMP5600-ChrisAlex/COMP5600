#!/usr/bin/python


import array
from ui import UI
from gameconstants import *


class Board:

    def __init__(self, cols, starting_pebbles, player1=None, player2=None):
        self.cols=cols
        self.startPebs = starting_pebbles

        if player1==None and player2==None:
            self.p1=array.array("I",(starting_pebbles,)*cols)
            #self.p1=array.array("I",range(1,cols+1))

            self.p2=array.array("I")
            self.p2.extend(self.p1)
        else:
            self.p1 = array.array("I",(0,)*cols)
            self.p2=array.array("I")
            self.p2.extend(self.p1)
            #copy values by value
            for i in range(0, cols):
                self.p1[i] = player1[i]
                self.p2[i] = player2[i]
            

    def getCols(self):
        return self.cols

    def __len__(self):
        return self.cols

    def move(self,player,bin):  

        movefrom = None
        moveto = None
        bin = bin -1; #array is 0-index, but paramater is not

        if bin < 0 or bin >= self.cols:
            raise IndexError("Invalid Bin")

        # create new board state
        newBoardState = Board(self.cols, self.startPebs, self.p1, self.p2)

        # determine which player
        if player == TOP_PLAYER:
            movefrom = newBoardState.getPlayer1()
            moveto   = newBoardState.getPlayer2()
        elif player == BOTTOM_PLAYER:
            movefrom = newBoardState.getPlayer2()
            moveto   = newBoardState.getPlayer1()
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
            raise IndexError("Invalid Bin")

        if player == TOP_PLAYER:
            return self.p1[bin-1]
        elif player == BOTTOM_PLAYER:
            return self.p2[bin-1]
        else:
            raise ValueError("Invalid Player")

    def isEquivalent(self, boardState):
        if boardState.p1 == self.p1:
            if boardState.p2 == self.p2:
                return True
        return False

    def isWon(self):
        p1Sum = 0
        p2Sum = 0
        for i in range(0, cols):
            p1Sum = p1Sum + self.p1[i]
            p2Sum = p2Sum + self.p2[i]
        if p1Sum == 0 or p2Sum == 0:
            return True
        else:
            return False

    def getPlayer1(self):
        return self.p1

    def getPlayer2(self):
        return self.p2
        
    def toString(self):
        
        s1 = "|"
        s2 = "|"

        for i in self.p1.tolist():
            s1 += '{:^4n}|'.format(i)

        #does not actually reverese list, just provides a reverse iterator
        for i in reversed(self.p2.tolist()): 
            s2 += '{:^4n}|'.format(i)

        return s1 + "\n|" + "-" * ( (5*len(l1)) - 1 ) + "|\n" + s2

    def __str__(self):
        return self.toString()



