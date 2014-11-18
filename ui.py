#!/usr/bin/python

import curses

import gameconstants 




class UI:
    #constant stdscr
    stdscr = None;

    #User values


    #define some constants which define where things are placed on the screen
    _boardrow = 2          #row which to print the board
    _boardcol = 2          #col which to print the board
    _boardbinsize = 4      #how large each bin of the board is

    _debugstart = 10

    @staticmethod
    def debug(s):
        if gameconstants.DEBUG:
            if UI.stdscr == None:
                print s
            else:
                UI.stdscr.move(UI._debugstart,0)
                UI.stdscr.insertln()
                UI.stdscr.insstr(s)
 
    @staticmethod
    def userError(s, line=9):
        if UI.stdscr == None:
            print s
        else:
            UI.stdscr.move(line,0)
            UI.stdscr.clrtoeol()
            UI.stdscr.insstr(s,curses.color_pair(2))
 


    def __init__(self, screen, askuser=True):

        if UI.stdscr == None:
            UI.stdscr = screen
        else:
            raise RuntimeError("UI is already initalized!")


        curses.noecho()
	curses.start_color()
	curses.use_default_colors()

	curses.init_pair(1,curses.COLOR_BLUE, -1)
	curses.init_pair(2,curses.COLOR_RED, -1)
	curses.init_pair(3,curses.COLOR_GREEN, -1)

        #clear the screen
        UI.stdscr.erase()

	curses.curs_set(0)
        UI.stdscr.move(UI._debugstart,0)
        UI.stdscr.leaveok(0)

        self.boardWin = None

        if askuser: self.askSetupQuestions()


    def numberInput(self,row,col,size,min,max):
        s = ""
        s = UI.stdscr.getstr(row,col,size)
        while (not s.isdigit()) or ( int(s) < min or int(s) > max ):
            UI.userError("You must enter a number between %d and %d!" % (min,max))
            UI.stdscr.move(row,col)
            UI.stdscr.clrtoeol()
            s = UI.stdscr.getstr(row,col,size)
        UI.userError("")
        return int(s)

    def optionInput(self,row,col,size,options):
        s = ""
        good = False
        while not good:
            s = UI.stdscr.getstr(row,col,size).lower()
            for opt in options: 
                if s == opt[:len(s)]:
                    UI.stdscr.addstr(row,col,opt)
                    good = True
                    UI.userError("");
                    return opt

            err = "You just enter one of: "
            for opt in options:
                err += opt[0] + "[" + opt[1:] + "], "
            UI.userError(err);
            UI.stdscr.move(row,col)
            UI.stdscr.clrtoeol()

    def askSetupQuestions(self):

        UI.stdscr.erase()

        UI.stdscr.addstr(1,1, "Number of Rows    : ")
        UI.stdscr.addstr(2,1, "Number of Pebbles : ")
        UI.stdscr.addstr(3,1, "P1 [human/comp]   : " ,curses.color_pair(2))
        UI.stdscr.addstr(4,1, "P2 [human/comp]   : " ,curses.color_pair(3))
        UI.stdscr.addstr(5,1, "Number of Plys    : ")
        UI.stdscr.addstr(6,1, "Run/Step          : ")
        
        UI.stdscr.move(1,21)
	curses.curs_set(1)
        curses.echo()

        UI.stdscr.noutrefresh()
        curses.doupdate()
    
        #get Number of Rows

        gameconstants.numRows = self.numberInput(1,21,2,2,10)

        #get Number of Pebbles
        gameconstants.numPebbles = self.numberInput(2,21,4,0,1000)

        #get P1 human/comp
        s = self.optionInput(3,21,8,["human", "computer"])
        if s == "human": gameconstants.p1Human = True
        else:            gameconstants.p1Human = False

        #get P2 human/comp
        s = self.optionInput(4,21,8,["human", "computer"])
        if s == "human": gameconstants.p2Human = True
        else:            gameconstants.p2Human = False

        #get numPlys
        numPlys = self.numberInput(5,21,3,1,50)
        
        #get run/step
        s = self.optionInput(6,21,5,["run", "step"])
        if s == "run": gameconstants.stepThrough = True
        else:          gameconstants.stepThrough = False


        curses.noecho()
        UI.stdscr.erase()

	curses.curs_set(0)
        UI.stdscr.move(UI._debugstart,0)
        UI.stdscr.leaveok(0)

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
        
            self.boardWin = UI.stdscr.derwin(5, (gameconstants.numRows * ( UI._boardbinsize + 1)) + 1,
                                    UI._boardrow, UI._boardcol) 

            self.boardWin.leaveok(0)
	    self.boardWin.attron(curses.color_pair(1))
            self._drawGrid();

        #put the numbers in their cells
        for i in range(1,len(board)+1):
            self.boardWin.addnstr(1,1+((i-1)*(UI._boardbinsize+1)),
                          '{0:^{width}n}'.format(
                          board.getBin(gameconstants.TOP_PLAYER,i),
                          width=UI._boardbinsize),
                          UI._boardbinsize, curses.color_pair(2))

            self.boardWin.addnstr(3,1+((i-1)*(UI._boardbinsize+1)),
                          '{0:^{width}n}'.format(
                          board.getBin(gameconstants.BOTTOM_PLAYER,len(board)+1-i),
                          width=UI._boardbinsize),
                          UI._boardbinsize, curses.color_pair(3))

        self.boardWin.noutrefresh()
        curses.doupdate()


    def __del__(self): #note: del is not gaurenteed to be called
        curses.endwin()



