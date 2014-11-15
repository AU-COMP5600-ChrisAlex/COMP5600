#!/usr/bin/python

from board import *
from ui import UI
import curses



def startProg(screen):
    b = Board(10,4);
    ui = UI(screen);
    ui.drawState(b)

    UI.stdscr.getch()

    b.move(TOP_PLAYER, 4)
    ui.drawState(b)

    UI.stdscr.getch()


    



if __name__ == "__main__":
    curses.wrapper(startProg)
    
   
