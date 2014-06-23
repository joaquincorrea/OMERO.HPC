#!/bin/sh

#$ -N tfmq_test
##$ -l exclusive.c
#$ -pe pe_16 16
#$ -V
#$ -cwd
#$ -l h_rt=00:10:00
#$ -l ram.c=8G

module load python 
# module load taskfarmermq
# module load taskfarmermq/2.1

cd $SGE_O_WORKDIR 

export PATH=$PATH:$(pwd)

for i in {1..16}
do
    ./tfmq-worker -b 5 -t 60 -q tfmqtaskqueue &
done
wait

##
## To start the client, 
## ./tfmq-client -i taskEnv.lst -w 0 -r 1 -q tfmqtaskqueue
##
