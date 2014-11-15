#!/usr/bin/python

from board import *
from gameconstants import *
from ui import UI
import curses



def startProg(screen):
    

    ui = UI(screen);

    b = Board(10,4);

    #ui.drawState(b)

    UI.stdscr.getch()

    #b.move(TOP_PLAYER, 4)
    #ui.drawState(b)

    #UI.stdscr.getch()


    



if __name__ == "__main__":
    curses.wrapper(startProg)
    
   
