#!/bin/bash -l

#PBS -t 1-100
#PBS -l nodes=1:ppn=4
#PBS -l walltime=00:04:00
#PBS -e part1/myjob.err
#PBS -o part1/myjob.out
#PBS -N LD_Part1_Job_array

N_SAMPLES=100
DEST_DIR="$HOME/part1"

echo "Running job on $HOST - " `date`

module load Python matplotlib


cd $HOME
mkdir -p "${DEST_DIR}"

python3 $HOME/git/exam/src/part1.py -n $N_SAMPLES --save "${DEST_DIR}/part1-${N_SAMPLES}-${PBS_ARRAYID}.pickle"

echo "Done"
