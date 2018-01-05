#!/bin/bash -l

#PBS -t 1-10
#PBS -l nodes=1:ppn=4
#PBS -l walltime=00:01:00
#PBS -e myjob.err
#PBS -o myjob.out
#PBS -N Part1_Job

N_SAMPLES=100

echo "Running job on $HOST - " `date`

module load Python matplotlib

cd $WORKDIR

python3 $HOME/git/exam/src/part1.py -n $N_SAMPLES --save "$WORKDIR/part1-${N_SAMPLES}-${PBS_ARRAYID}.pickle"

echo "Done"
