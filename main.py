#!/usr/bin/python

from board import *
import gameconstants
from ui import UI
import curses
import alpha_beta
import human_player
import and_or_player
import sys, getopt
import os, stat
import time


askUser = True

def startProg(screen):
    
    global askUser

    if not gameconstants.ghost:
        ui = UI(screen,askUser)

    if not askUser:
        if gameconstants.p1 == None:
           gameconstants.p1 = human_player.Human_Player(gameconstants.TOP_PLAYER, ui) 
        if gameconstants.p2 == None:
           gameconstants.p2 = human_player.Human_Player(gameconstants.BOTTOM_PLAYER, ui) 

    if gameconstants.p1 == None: raise RuntimeError("P1 cannot be None!")           
    if gameconstants.p2 == None: raise RuntimeError("P2 cannot be None!")           

    b = Board();
    if not gameconstants.ghost:
        ui.drawState(b)
    else:
        UI.printInstructions("Ghost Mode")

    plyCount = 0
    starttime = time.time()
    startcputime = time.clock()
    while True:
        #check to see if we should pause before we move
        if not gameconstants.ghost: ui.printTurn(gameconstants.p1)

        if gameconstants.stepThrough and gameconstants.p1.isComputer():
            pause()
        b = b.move(gameconstants.p1.player, gameconstants.p1.move(b))
        plyCount = plyCount + 1

        if not gameconstants.ghost: ui.drawState(b)

        if b.isWon():
            endtime = time.time()
            endcputime = time.clock()
            if not gameconstants.ghost: ui.printWinMessage(b.whoWon())
            pause()
            break

        if not gameconstants.ghost: ui.printTurn(gameconstants.p2)
        if gameconstants.stepThrough and gameconstants.p2.isComputer():
            pause()
        b = b.move(gameconstants.p2.player, gameconstants.p2.move(b))
        plyCount = plyCount + 1
        if not gameconstants.ghost: ui.drawState(b)

        if b.isWon():
            endtime = time.time()
            endcputime = time.clock()
            if not gameconstants.ghost: ui.printWinMessage(b.whoWon())
            pause()
            break

        if plyCount > 10000:
            #assume infinite loop 
            endtime = time.time()
            endcputime = time.clock()
            break


    if not gameconstants.ghost:
        curses.endwin()
    try:
        #output some statistics
        statFile = open(gameconstants.statsFile, "a")
        if os.stat(gameconstants.statsFile)[stat.ST_SIZE]==0:
            #print the header
            statFile.write("Rows,Pebbles,P1,P2,Depth,Runtime,CPU time,plycount,winner\n");

        #print the statistics
        statFile.write(str(gameconstants.numRows) + ",")          #rows
        statFile.write(str(gameconstants.numPebbles) + ",")       #pebbles
        statFile.write(str(gameconstants.p1.optName()) + ",")     #p1
        statFile.write(str(gameconstants.p2.optName()) + ",")     #p2
        statFile.write(str(gameconstants.numPlys) + ",")          #depth
        statFile.write(str(endtime-starttime) + ",")              #runtime
        statFile.write(str(endcputime-startcputime) + ",")        #CPU time
        statFile.write(str(plyCount)+ ",")                        #plycount
        if b.whoWon() == gameconstants.TOP_PLAYER:                #winner
            statFile.write(str(gameconstants.p1.optName()) + ",")
        elif b.whoWon() == gameconstants.BOTTOM_PLAYER:
            statFile.write(str(gameconstants.p2.optName()) + ",")
        else:
            statFile.write("?" + ",")

        statFile.write("\n")
        statFile.flush()
        statFile.close()
    except Exception as e:
        print "Problem writing stats file!"
        print e

    print "------------------------------------"
    print "END OF GAME STATISTICS:"
    print "Rows    : ", gameconstants.numRows
    print "Pebbles : ", gameconstants.numPebbles
    print "P1      : ", gameconstants.p1.optName()
    print "P2      : ", gameconstants.p2.optName()
    print "Depth   : ", gameconstants.numPlys
    print "Runtime : ", str(endtime-starttime)
    print "CPUtime : ", str(endcputime-startcputime)
    print "plycount: ", plyCount

    if b.whoWon() == gameconstants.TOP_PLAYER: 
        print "winner  : ", str(gameconstants.p1.optName())
    elif b.whoWon() == gameconstants.BOTTOM_PLAYER:
        print "winner  : ", str(gameconstants.p2.optName())
    else:
        print "winner  : ?"
    print "------------------------------------"


def pause(s="Press any key to continue..."):
    if not gameconstants.ghost:
        UI.printInstructions(s)
        c = UI.stdscr.getch()
        UI.clearInstructions()


def usage(): 
    print "-h [--help]        : Print this message"  
    print "-d [--defaults]    : For debug. Sets user input values to defaults, does not ask for input"
    print "-p [--numplys=]    : Specify the number of Plys.    Argument is [1-50]"
    print "-r [--numrows=]    : Specify the number of rows.    Argument is [2-10]"
    print "-e [--numpebbles=] : Specify the number of pebbles. Argument is [0-1000]"
    print "-s [--step]        : Step through game"
    print "-g [--run]         : Do not step through game (go)"
    print "-t [--p1=]         : Specify player 1 ([t]op player).     Options are: [human, minmax, andor]"
    print "-b [--p2=]         : Specify player 2 ([b]ottom player).  Options are: [human, minmax, andor]"
    print "-z [--ghost]       : Run without a UI. Must specify all other options and -r to use ghost mode"

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hdp:r:e:sgt:b:z",["help","defaults","numplys=", "numrows=", "numpebbles=", "step","run","p1=","p2=","ghost"])
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
            gameconstants.p1 = alpha_beta.Alpha_Beta_Player(gameconstants.TOP_PLAYER) 
            gameconstants.p2 = None 
            gameconstants.numPlys = 4
            gameconstants.stepThrough = True
            askUser = False
            UI.debug("Using default game paramaters:")
            break
        elif opt in ("-p", "--numplys"):
            gameconstants.numPlys = int(arg)
        elif opt in ("-r", "--numrows"):
            gameconstants.numRows = int(arg) 
        elif opt in ("-e", "--numpebbles"):
            gameconstants.numPebbles = int(arg)
        elif opt in ("-s", "--step"):
            if gameconstants.stepThrough == None:
                gameconstants.stepThrough  = True
            else:
                print "You cannot specify both --run (-g) and --step (-s)!"
                sys.exit(2)
        elif opt in ("-g", "--run"):
            if gameconstants.stepThrough == None:
                gameconstants.stepThrough  = False
            else:
                print "You cannot specify both --run (-g) and --step (-s)!"
                sys.exit(2)
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
                elif s == "andor":  gameconstants.p2 = and_or_player.And_Or_Player(gameconstants.BOTTOM_PLAYER)
                elif s == "minmax": gameconstants.p2 = alpha_beta.Alpha_Beta_Player(gameconstants.BOTTOM_PLAYER)
            else:
                print "Invalid argument: ", arg, " for option ", opt
                print "\tValid arguments are: [human, minmax, andor]"
                sys.exit(2)
        elif opt in ("-z", "--ghost"):
            gameconstants.ghost= True
        else:
            print "Unrecognized option: ", opt
            usage()
            sys.exit()


    if gameconstants.ghost:
        #make sure everything is specified
        if (gameconstants.numPlys == 0 or
            gameconstants.numRows == 0 or
            gameconstants.numPebbles == 0 or
            gameconstants.p1 == None or
            gameconstants.p2 == None or
            gameconstants.stepThrough != False):
          print "ERROR: when using ghost mode, you must specify all game paramaters, and be in 'go' mode!"
          sys.exit(2)


  
    try:
        if not gameconstants.ghost:
            curses.wrapper(startProg)
        else:
            startProg(None)
    except KeyboardInterrupt:
        print "Keyboard Interrupt"





