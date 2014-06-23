#!/bin/bash -l

module load python
# module load taskfarmermq/2.1

export PATH=$PATH:$(pwd)

for i in {1..8}
do
    # tfmq-worker -b 3 -t 30 -q tfmqtaskqueue &
    ./tfmq-worker -b 3 -t 10 &
    #sleep 2
done
wait

##
## To start the client, 
## tfmq-client -i taskEnv.lst -w 0 -r 1 -q tfmqtaskqueue
##