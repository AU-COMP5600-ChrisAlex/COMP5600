#!/usr/bin/python

from board import *
import gameconstants
from ui import UI
import curses
import alpha_beta
import human_player
import and_or_player



def startProg(screen):
    

    ui = UI(screen);
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
    try:
        curses.wrapper(startProg)
    except KeyboardInterrupt:
        print "Keyboard Interrupt"

