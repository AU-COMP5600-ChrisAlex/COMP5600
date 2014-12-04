#/bin/bash


#script to run the program alot to gather runtime statistics


#format: ./main.py -p [depth] -r [rows] -e [pebbles] -t [top_alg] -b [bot_alg] -g --ghost





#runs 10 times (for statistical reasons), with specified options
#runs with players in both positions

#makeRun [depth] [rows] [pebbles] [top_player] [bottom_player]

trap "pkill -f makeRun; pkill -f main.py; exit" SIGHUP SIGINT SIGTERM

makeRun() {
   for i in $(seq 1 10); do
       ./main.py -p $1 -r $2 -e $3 -t minmax -b andor  -g --ghost
       ./main.py -p $1 -r $2 -e $3 -t andor  -b minmax -g --ghost
   done
}


export -f makeRun


#different depths
for depth in $(seq 1 9); do
    for rows in $(seq 3 10); do
        seq 1 10 | xargs -P 8 -i -n 1 bash -c "makeRun $depth $rows {}"
    done
done







