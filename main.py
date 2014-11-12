#!/usr/bin/python

from board import *
from ui import UI



b = Board(10,4);
ui = UI();
ui.drawState(b)

UI.stdscr.getch()

b.move(TOP_PLAYER, 4)
ui.drawState(b)

UI.stdscr.getch()


