#!/bin/sh

#$ -S /bin/bash
#$ -V
#$ -cwd
#$ -notify
##$ -j y -o worker.$TASK_ID.log
#$ -l high.c
#$ -N tfmq_test
#$ -l h_rt=00:10:00
#$ -l ram.c=1G
#$ -pe pe_1 1

START=$(date +%s)

module load python
# module load taskfarmermq
# module load taskfarmermq/2.1

#for i in {1..8}
#do
#   echo "start worker $i"
#   #tfmq-worker -q taskenv -b 5 &
#   tfmq-worker -b 5 -t 60 -q tfmqtaskqueue &
#done
#wait

./tfmq-worker -b 5 -t 60 -q tfmqtaskqueue 

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds"

##
## To start the client, 
## tfmq-client -i taskEnv.lst -w 0 -r 1 -q tfmqtaskqueue
##
