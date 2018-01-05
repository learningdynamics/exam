#! /bin/bash


NUM=5
N=2

for i in $(seq 1 $NUM) ; do
    python3 part1.py -n $N --save "part1-${N}-${i}.pickle"
done
