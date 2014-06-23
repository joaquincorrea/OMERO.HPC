#!/bin/bash

#$ -S /bin/bash
#$ -cwd
#$ -l normal.c
#$ -l h_rt=00:10:00
#$ -l ram.c=1G
#$ -t 1:5

module load python
# module load taskfarmermq
# module load taskfarmermq/2.1

./tfmq-worker -b 5 -t 60 -q tfmqtaskqueue

##
## To start the client, 
## ./tfmq-client -i taskEnv.lst -w 0 -r 1 -q tfmqtaskqueue
##
