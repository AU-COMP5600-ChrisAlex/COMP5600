#!/usr/bin/python

import curses
import atexit

TOP_PLAYER    = 0
BOTTOM_PLAYER = 1

DEBUG = True

class UI:
    #constant stdscr
    stdscr = None;


    #define some constants which define where things are placed on the screen
    _boardrow = 2          #row which to print the board
    _boardcol = 2          #col which to print the board
    _boardbinsize = 4      #how large each bin of the board is

    _debugstart = 10


    def __init__(self):


        if UI.stdscr == None:
            #if the program crashes, make sure we end curses
            atexit.register(curses.endwin)

            #begin curses
            UI.stdscr = curses.initscr()
            curses.noecho()

        #clear the screen
        UI.stdscr.erase()

        self.boardWin = None

    @staticmethod
    def debug(s):
        if DEBUG:
            if UI.stdscr == None:
                print s
            else:
                UI.stdscr.move(UI._debugstart,0)
                UI.stdscr.insertln()
                UI.stdscr.insstr(s)
        
    def _drawGrid(self):
        self.boardWin.border()

        rows,cols=self.boardWin.getmaxyx()

        self.boardWin.hline(2,1,curses.ACS_HLINE,cols-2)
        self.boardWin.addch(2,0, curses.ACS_LTEE)
        self.boardWin.addch(2,cols-1, curses.ACS_RTEE)


        #for each cell, place the vertical lines
        for i in range(1+UI._boardbinsize,cols-1,UI._boardbinsize+1):
            self.boardWin.addch(0,i,curses.ACS_TTEE)
            self.boardWin.addch(1,i,curses.ACS_VLINE)
            self.boardWin.addch(2,i,curses.ACS_PLUS)
            self.boardWin.addch(3,i,curses.ACS_VLINE)
            self.boardWin.addch(4,i,curses.ACS_BTEE)


    def drawState(self, board):
        #make a sub-window for the board
        if self.boardWin == None:
            self.boardWin = UI.stdscr.subwin(5, (len(board) * ( UI._boardbinsize + 1)) + 1,
                                    UI._boardrow, UI._boardcol) 
            self._drawGrid();

        #put the numbers in their cells
        for i in range(1,len(board)+1):
            self.boardWin.addnstr(1,1+((i-1)*(UI._boardbinsize+1)),
                          '{0:^{width}n}'.format(
                          board.getBin(TOP_PLAYER,i),
                          width=UI._boardbinsize),
                          UI._boardbinsize)

            self.boardWin.addnstr(3,1+((i-1)*(UI._boardbinsize+1)),
                          '{0:^{width}n}'.format(
                          board.getBin(BOTTOM_PLAYER,len(board)+1-i),
                          width=UI._boardbinsize),
                          UI._boardbinsize)

        self.boardWin.noutrefresh()
        curses.doupdate()


    def __del__(self): #note: del is not gaurenteed to be called
        curses.endwin()
        #only available in python 3
        #atexit.unregister(curses.endwin)



