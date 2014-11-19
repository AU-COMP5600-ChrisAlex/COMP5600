#!/usr/bin/python

from board import *
import gameconstants
from ui import UI
import curses
import alpha_beta
import human_player
import and_or_player
import sys, getopt


askUser = False

def startProg(screen):
    
    global askUser

    ui = UI(screen,askUser);
    b = Board();
    ui.drawState(b)


    p1 = alpha_beta.Alpha_Beta_Player(gameconstants.TOP_PLAYER) 
    p2 = human_player.Human_Player(gameconstants.BOTTOM_PLAYER, ui) 

    c = '' 
    while c != ord('q'):
        c = UI.stdscr.getch()
        b = b.move(p1.player, p1.move(b))
        ui.drawState(b)


    
    #b = b.move(gameconstants.TOP_PLAYER, 4)
    #ui.drawState(b)
    #UI.stdscr.getch()


if __name__ == "__main__":
    global askUser

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv,"hd",["help","defaults"])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print "-h [--help]    : Print this message"  
            print "-d [defaults]  : For debug. Sets user input values to defaults"
            sys.exit()
        elif opt in ("-d", "--defaults"):
            gameconstants.numRows = 4 
            gameconstants.numPebbles = 4
            gameconstants.p1Human = False
            gameconstants.p2Human = False
            gameconstants.numPlys = 4
            gameconstants.stepThrough = False
            askUser = False

    try:
        curses.wrapper(startProg)
    except KeyboardInterrupt:
        print "Keyboard Interrupt"

