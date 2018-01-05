#! /bin/csh

#PBS -l nodes=1:ppn=8
#PBS -l walltime=00:10:00
#PBS -o myjob.out
#PBS -N Part1_Job

echo "Running job on $HOST - " `date`

module load Python matplotlib

python3 $HOME/git/exam/src/ -n 10 --plot $WORKDIR/part1_plot.png --latex $WORKDIR/part1_latex.tex

echo "Done"
