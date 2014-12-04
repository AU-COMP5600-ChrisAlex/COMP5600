#!/bin/bash


#script to run the program alot to gather runtime statistics


#format: ./main.py -p [depth] -r [rows] -e [pebbles] -t [top_alg] -b [bot_alg] -g --ghost






for i in $(seq 1 10); do
    ./main.py -p 4 -r 4 -e 4 -t minmax -b andor -g --ghost
done
