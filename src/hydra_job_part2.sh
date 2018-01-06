#!/bin/bash -l

#PBS -t 1-5
#PBS -l nodes=1:ppn=4
#PBS -l walltime=00:20:00
#PBS -e part2/myjob.err
#PBS -o part2/myjob.out
#PBS -N LD_Part2_Job_array

N_SAMPLES=100
N_SAMPLES_JAL=5
DEST_DIR="$HOME/part2"

echo "Running job on $HOST - " `date`

module load Python matplotlib


cd $HOME
mkdir -p "${DEST_DIR}"

python3 $HOME/git/exam/src/part2.py -n $N_SAMPLES -njal $N_SAMPLES_JAL --save "${DEST_DIR}/part2-${USER}-${N_SAMPLES}-${PBS_ARRAYID}.pickle"

echo "Done"