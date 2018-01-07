#!/bin/bash -l

#PBS -t 1-40
#PBS -l nodes=1:ppn=4
#PBS -l walltime=08:00:00
#PBS -e part3/myjob.err
#PBS -o part3/myjob.out
#PBS -N LD_Part3_Job_array


DEST_DIR="$HOME/part3"

echo "Running job on $HOST - " `date`

module load Python matplotlib


cd $HOME
mkdir -p "${DEST_DIR}"

python3 $HOME/git/exam/src/part3.py --save "${DEST_DIR}/part3-${USER}-${PBS_ARRAYID}.pickle"

echo "Done"
