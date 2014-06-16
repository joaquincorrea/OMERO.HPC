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
#$ -pe pe_8 8

export TFMQ_START=$(date +%s)
echo "Start time = $TFMQ_START"

module load python
# module load taskfarmermq
# module load taskfarmermq/2.1

for i in {1..8}
do
   echo "start worker $i"
   ./tfmq-worker -b 5 -t 0 &
done
wait

TFMQ_END=$(date +%s)
echo "End time = $TFMQ_END"

DIFF=$(( $TFMQ_END - $TFMQ_START ))
echo "It took $DIFF seconds"
echo "$(($DIFF / 60)) minutes and $(($DIFF % 60)) seconds elapsed."

##
## To start the client, 
## ./tfmq-client -i taskEnv.lst -w 0 -r 1 -q tfmqtaskqueue
##
