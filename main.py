#!/usr/bin/python

from board import *
import gameconstants
from ui import UI
import curses



def startProg(screen):
    
    ui = UI(screen);
    b = Board();







    ui.drawState(b)

    UI.stdscr.getch()
    
    b = b.move(gameconstants.TOP_PLAYER, 4)

    ui.drawState(b)

    UI.stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(startProg)
    
   
