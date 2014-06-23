#!/bin/sh

#$ -S /bin/bash
#$ -V
#$ -cwd
#$ -notify
##$ -P prok-IMG.p
#$ -j y -o worker.$TASK_ID.log
#$ -l normal.c
#$ -N tfmq_test
#$ -l h_rt=00:30:00
#$ -l ram.c=1G
#$ -pe pe_slots 8

module load python
# module load taskfarmermq
# module load taskfarmermq/2.1

for i in {1..8}
do
   echo "start worker $i"
   ./tfmq-worker -b 5 -t 60 -q tfmqtaskqueue &
done
wait

##
## To start the client, 
## ./tfmq-client -i taskEnv.lst -w 0 -r 1 -q tfmqtaskqueue
##
