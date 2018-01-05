#!/bin/bash -l

#PBS -l nodes=1:ppn=8
#PBS -l walltime=00:10:00
#PBS -e myjob.err
#PBS -o myjob.out
#PBS -N Part1_Job

N_SAMPLES=1000

echo "Running job on $HOST - " `date`

module load Python matplotlib

cd $WORKDIR

python3 $HOME/git/exam/src/part1.py -n $N_SAMPLES --plot $WORKDIR/part1_plot_${N_SAMPLES}.png --latex $WORKDIR/part1_latex_${N_SAMPLES}.tex

echo "Done"
