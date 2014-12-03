#!/usr/bin/python

import curses

import gameconstants 
import and_or_player
import alpha_beta


class UI:
    #constant stdscr
    stdscr = None;

    #color constants
    BLUE_PAIR    = 1
    RED_PAIR     = 2
    GREEN_PAIR   = 3

    BOARD_P_COLOR = BLUE_PAIR
    TOP_P_COLOR   = RED_PAIR 
    BOT_P_COLOR   = GREEN_PAIR 



    #define some constants which define where things are placed on the screen
    _boardbinsize = 4      #how large each bin of the board is

    _boardrow = 3          #row which to print the board
    _boardcol = 2          #col which to print the board

    _debugstart = 10
    _instructline = 1
    _instructcol = 2

    @staticmethod
    def debug(s):
        if gameconstants.DEBUG:
            if UI.stdscr == None:
                print s
            else:
                UI.stdscr.move(UI._debugstart,0)
                UI.stdscr.insertln()
                UI.stdscr.insstr(str(s))
 
    @staticmethod
    def userError(s, line=9):
        if UI.stdscr == None:
            print s
        else:
            UI.stdscr.move(line,0)
            UI.stdscr.clrtoeol()
            UI.stdscr.insstr(s,curses.color_pair(UI.RED_PAIR))
 


    def __init__(self, screen, askuser=True):

        if UI.stdscr == None:
            UI.stdscr = screen
        else:
            raise RuntimeError("UI is already initalized!")


        curses.noecho()
	curses.start_color()
	curses.use_default_colors()

	curses.init_pair(UI.BLUE_PAIR ,curses.COLOR_BLUE, -1)
	curses.init_pair(UI.RED_PAIR  ,curses.COLOR_RED, -1)
	curses.init_pair(UI.GREEN_PAIR,curses.COLOR_GREEN, -1)

        #clear the screen
        UI.stdscr.erase()

	curses.curs_set(0)
        UI.stdscr.move(UI._debugstart,0)
        UI.stdscr.leaveok(0)

        self.boardWin = None

        if askuser: self.askSetupQuestions()


    def clearInstructions(self):
        UI.stdscr.move(UI._instructline,0)
        UI.stdscr.clrtoeol()

    #prints a line at the top of the screen, telling the user what to do
    def printInstructions(self, str):
        self.clearInstructions()
        UI.stdscr.move(UI._instructline, UI._instructcol)
        UI.stdscr.addstr(str)


    def numberInput(self,row,col,size,min,max):
        UI.stdscr.move(row,col)
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

        UI.stdscr.addstr(1,1, "Number of Rows              : ")
        if gameconstants.numRows!= 0:
            UI.stdscr.addstr(1, 31, gameconstants.numRows)
        UI.stdscr.addstr(2,1, "Number of Pebbles           : ")
        if gameconstants.numPebbles != 0:
            UI.stdscr.addstr(2, 31, gameconstants.numPebbles)
        UI.stdscr.addstr(3,1, "P1 [human/minmax/andor]     : " ,curses.color_pair(UI.TOP_P_COLOR))
        UI.stdscr.addstr(4,1, "P2 [human/minmax/andor]     : " ,curses.color_pair(UI.BOT_P_COLOR))
        UI.stdscr.addstr(5,1, "Number of Plys              : ")
        if gameconstants.numPlys != 0:
            UI.stdscr.addstr(5, 31, gameconstants.numPlys)
        UI.stdscr.addstr(6,1, "Run/Step                    : ")
        if gameconstants.stepThrough != None:
            if gameconstants.stepThrough:
                UI.stdscr.addstr(6,31, "Step") 
            else: UI.stdscr.addstr(6,31, "Run") 

        
        UI.stdscr.move(1,31)
	curses.curs_set(1)
        curses.echo()

        UI.stdscr.noutrefresh()
        curses.doupdate()
    
        #get Number of Rows, if not already set
        if gameconstants.numRows == 0:
            gameconstants.numRows = self.numberInput(1,31,2,2,10)

        #get Number of Pebbles
        if gameconstants.numPebbles == 0:
            gameconstants.numPebbles = self.numberInput(2,31,4,0,1000)

        #get P1 human/comp
        s = self.optionInput(3,31,8,["human", "minmax", "andor"])
        if   s == "human":  gameconstants.p1 = human_player.Human_Player(gameconstants.TOP_PLAYER, self) 
        elif s == "andor":  gameconstants.p1 = and_or_player.And_Or_Player(gameconstants.TOP_PLAYER)
        elif s == "minmax": gameconstants.p1 = alpha_beta.Alpha_Beta_Player(gameconstants.TOP_PLAYER)
        else: raise RuntimeError("optionInput failed to return a valid value!")           

        #get P2 human/comp
        s = self.optionInput(4,31,8,["human", "minmax", "andor"])
        if   s == "human":  gameconstants.p2 = human_player.Human_Player(gameconstants.BOTTOM_PLAYER, self) 
        elif s == "andor":  gameconstants.p2 = and_or_player.And_Or_Player(gameconstants.BOTTOM_PLAYER)
        elif s == "minmax": gameconstants.p2 = alpha_beta.Alpha_Beta_Player(gameconstants.BOTTOM_PLAYER)
        else: raise RuntimeError("optionInput failed to return a valid value!")           

        #get numPlys
        if gameconstants.numPlys == 0:
            gameconstants.numPlys = self.numberInput(5,31,3,1,50)
        
        #get run/step
        if gameconstants.stepThrough == None:
            s = self.optionInput(6,31,5,["run", "step"])
            if s == "run": gameconstants.stepThrough = True
            else:          gameconstants.stepThrough = False


        curses.noecho()
        UI.stdscr.erase()

	curses.curs_set(0)
        UI.stdscr.move(UI._debugstart,0)
        UI.stdscr.leaveok(0)

    def refreshBoardWin(self):
        self.boardWin.noutrefresh()
        curses.doupdate()

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
            if(gameconstants.numRows < 1): raise ValueError("gameconstants.numRows too small!")
        
            self.boardWin = UI.stdscr.derwin(5, (gameconstants.numRows * ( UI._boardbinsize + 1)) + 1,
                                    UI._boardrow, UI._boardcol) 

            self.boardWin.leaveok(0)
	    self.boardWin.attron(curses.color_pair(UI.BOARD_P_COLOR))
            self._drawGrid();

        #put the numbers in their cells
        for i in range(1,len(board)+1):
            self.boardWin.addnstr(1,1+((i-1)*(UI._boardbinsize+1)),
                          '{0:^{width}n}'.format(
                          board.getBin(gameconstants.TOP_PLAYER,i),
                          width=UI._boardbinsize),
                          UI._boardbinsize, curses.color_pair(UI.TOP_P_COLOR))

            self.boardWin.addnstr(3,1+((i-1)*(UI._boardbinsize+1)),
                          '{0:^{width}n}'.format(
                          board.getBin(gameconstants.BOTTOM_PLAYER,len(board)+1-i),
                          width=UI._boardbinsize),
                          UI._boardbinsize, curses.color_pair(UI.BOT_P_COLOR))

        self.refreshBoardWin()

    #select a cell
    def _selectCell(self, player, bin):
        #figure out which player we are, set which row to edit
        if player == gameconstants.TOP_PLAYER: row = 1
        elif player == gameconstants.BOTTOM_PLAYER: row = 3
        else: raise ValueErrror("Invalid Player")
    
        #change attributes of bin
        self.boardWin.chgat(row, 1+((bin-1)*(UI._boardbinsize+1)), UI._boardbinsize, curses.A_REVERSE)
        
    #unselect a cell
    def _unselectCell(self, player, bin):
        if player == gameconstants.TOP_PLAYER: 
            row = 1
            color = UI.TOP_P_COLOR
        elif player == gameconstants.BOTTOM_PLAYER: 
            row = 3
            color = UI.BOT_P_COLOR
        else: raise ValueErrror("Invalid Player")
        
        #change attributes of bin
        self.boardWin.chgat(row, 1+((bin-1)*(UI._boardbinsize+1)), UI._boardbinsize, curses.color_pair(color))

    #allows a human player to select a cell to move. Returns bin number.
    def interact(self, player, board=None):
        if self.boardWin == None:
            if board != None: self.drawState(board)
            else: raise RuntimeError("No board has been drawn yet!")

        self.printInstructions("Use the arrow keys or press a number to select a cell. Then press Enter to select");

        #first, select the player's first cell
        selected = 1
        newsel= 1
        self._selectCell(player,selected)
        self.refreshBoardWin()

        #now, allow arrow keys, [hl], and [0-9] to select new cell. Enter confirms

        done = False
        while not done:

            c = UI.stdscr.getch()

            #(windows compatible newline?)
            if c == ord('\n') or c == ord('\r'):

                #check to see if that is a valid selection (ie, non-zero value)
                if player == gameconstants.BOTTOM_PLAYER:
                    bin = board.getCols() - selected + 1
                else: bin = selected

                 
                if board.getBin(player,bin) == 0:
                    #invalid bin!
                    UI.userError("Illegal move!")
                    continue
                else:
                    #return current selection
                    self.clearInstructions()
                    return bin

            elif c == curses.KEY_LEFT or c == ord('h'):
                newsel = selected - 1
            elif c == curses.KEY_RIGHT or c == ord('l'): 
                newsel = selected + 1
            elif c >= ord('0') and c <= ord('9'):
                newsel = c - ord('0')
                if newsel == 0: newsel = 10
            else: continue

            UI.userError("")
            
            if newsel > gameconstants.numRows: newsel = gameconstants.numRows
            if newsel < 1: newsel = 1

            if newsel != selected:
                self._unselectCell(player, selected)
                self._selectCell(player, newsel)
                selected = newsel 
                self.refreshBoardWin()
                
                
    def __del__(self): #note: del is not gaurenteed to be called
        curses.endwin()




def _uitest(screen):

    gameconstants.numRows = 8 
    gameconstants.numPebbles = 5

    ui = UI(screen, False)
    b = Board()

    ui.drawState(b)

    bin = ui.interact(gameconstants.TOP_PLAYER)
    b = b.move(gameconstants.TOP_PLAYER, bin) 
    
    ui.drawState(b)
    UI.stdscr.getch()

if __name__ == "__main__":

    from board import *
    try:
        curses.wrapper(_uitest)
    except KeyboardInterrupt:
        print "Keyboard Interrupt"


