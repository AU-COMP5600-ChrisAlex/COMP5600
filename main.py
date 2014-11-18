#!/usr/bin/python

from board import *
import gameconstants
from ui import UI
import curses
import sys
import getopt


noask = False

def startProg(screen):
    global noask
    print noask
    sys.exit()

    
    ui = UI(screen, askuser=(not noask));
    b = Board();




    ui.drawState(b)

    UI.stdscr.getch()
    
    b = b.move(gameconstants.TOP_PLAYER, 4)

    ui.drawState(b)

    UI.stdscr.getch()



def usage():
    print " h --help     Print this message"
    print " r --rows=    Specify number of rows"
    print " n --noask    (debugging) UI does not ask for game paramaters"

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv, "hr:n", ["help", "rows=", "noask"])
    for opt, arg in opts:
        print opt

        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ('r', "--rows="):
            print "rows = ", arg
            print "NOT IMPLIMENTED"
        elif opt in ('n', "--noask"):
            noask = True
            gameconstants.numRows = 8
            gameconstants.numPebbles = 4
    except getopt.GetoptError:
        usage()
        sys.exit(2)


    sys.exit()

    curses.wrapper(startProg)
    
   
