#!/usr/bin/python

from board import *
import gameconstants
from ui import UI
import curses
import alpha_beta
import human_player
import and_or_player
import sys, getopt


askUser = True

def startProg(screen):
    
    global askUser

    ui = UI(screen,askUser);

    if not askUser:
        if gameconstants.p1 == None:
           gameconstants.p1 = human_player.Human_Player(gameconstants.TOP_PLAYER, ui) 
        if gameconstants.p2 == None:
           gameconstants.p2 = human_player.Human_Player(gameconstants.BOTTOM_PLAYER, ui) 

    if gameconstants.p1 == None: raise RuntimeError("P1 cannot be None!")           
    if gameconstants.p2 == None: raise RuntimeError("P2 cannot be None!")           

    b = Board();
    ui.drawState(b)

    while True:

        #check to see if we should pause before we move
        ui.printTurn(gameconstants.p1)
        if gameconstants.stepThrough and gameconstants.p1.isComputer():
            pause()
        b = b.move(gameconstants.p1.player, gameconstants.p1.move(b))
        ui.drawState(b)

        if b.isWon():
            ui.printWinMessage(b.whoWon)
            pause()
            break

        ui.printTurn(gameconstants.p2)
        if gameconstants.stepThrough and gameconstants.p2.isComputer():
            pause()
        b = b.move(gameconstants.p2.player, gameconstants.p2.move(b))
        ui.drawState(b)

        if b.isWon():
            ui.printWinMessage(b.whoWon)
            pause()
            break


def pause(s="Press any key to continue..."):
    UI.printInstructions(s)
    c = UI.stdscr.getch()
    UI.clearInstructions()


def usage(): 
    print "-h [--help]     : Print this message"  
    print "-d [--defaults]   : For debug. Sets user input values to defaults, does not ask for input"
    print "-p [--numplys=]    : Specify the number of Plys.    Argument is [1-50]"
    print "-r [--numrows=]    : Specify the number of rows.    Argument is [2-10]"
    print "-e [--numpebbles=] : Specify the number of pebbles. Argument is [0-1000]"
    print "-s [--step]        : Step through game"
    print "-t [--p1=]         : Specify player 1 ([t]op player).     Options are: [human, minmax, andor]"
    print "-b [--p2=]         : Specify player 2 ([b]ottom player).  Options are: [human, minmax, andor]"

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hdp:r:e:st:b:",["help","defaults","numplys=", "numrows=", "numpebbles=", "step", "p1=","p2="])
    except getopt.GetoptError as err:
        print str(err);
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-d", "--defaults"):
            gameconstants.numRows = 4 
            gameconstants.numPebbles = 4
            gameconstants.p1 = and_or_player.And_Or_Player(gameconstants.TOP_PLAYER) 
            gameconstants.p2 = None 
            gameconstants.numPlys = 4
            gameconstants.stepThrough = True
            askUser = False
            break
        elif opt in ("-p", "--numplys"):
            gameconstants.numPlys = arg
        elif opt in ("-r", "--numrows"):
            gameconstants.numRows = arg 
        elif opt in ("-e", "--numpebbles"):
            gameconstants.numPebbles = arg
        elif opt in ("-s", "--step"):
            gameconstants.stepThrough  = True
        elif opt in ("-t", "--p1"):
            s = arg.lower()
            if s in ["human", "minmax", "andor"]:
                if   s == "human":  gameconstants.p1 = ""
                elif s == "andor":  gameconstants.p1 = and_or_player.And_Or_Player(gameconstants.TOP_PLAYER)
                elif s == "minmax": gameconstants.p1 = alpha_beta.Alpha_Beta_Player(gameconstants.TOP_PLAYER)
            else:
                print "Invalid argument: ", arg, " for option ", opt
                print "\tValid arguments are: [human, minmax, andor]"
                sys.exit(2)
        elif opt in ("-b", "--p2"):
            s = arg.lower()
            if s in ["human", "minmax", "andor"]:
                if   s == "human":  gameconstants.p2 = ""
                elif s == "andor":  gameconstants.p2 = and_or_player.And_Or_Player(gameconstants.TOP_PLAYER)
                elif s == "minmax": gameconstants.p2 = alpha_beta.Alpha_Beta_Player(gameconstants.TOP_PLAYER)
            else:
                print "Invalid argument: ", arg, " for option ", opt
                print "\tValid arguments are: [human, minmax, andor]"
                sys.exit(2)
        else:
            print "Unrecognized option: ", opt
            usage()
            sys.exit()

  
    try:
        curses.wrapper(startProg)
    except KeyboardInterrupt:
        print "Keyboard Interrupt"





