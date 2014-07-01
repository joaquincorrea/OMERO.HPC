#!/bin/bash -l

# module load python
# module load taskfarmermq/2.1

#module load python_base
#export VENV=/project/projectdirs/ngbi/jobs/tfmq/python_test
#export TFMQ_PATH=/project/projectdirs/ngbi/jobs/tfmq
#
#source /project/projectdirs/ngbi/jobs/tfmq/python_test/bin/activate
#
#export PATH=$PATH:$(pwd)

for i in {1..8}
do
    # tfmq-worker -b 3 -t 30 -q tfmqtaskqueue &
#    /project/projectdirs/ngbi/jobs/tfmq/tfmq-worker
    $OMERO_HOME/lib/scripts/OMERO.HPC/resources/taskfarmermq/tfmq-worker -b 3 -t 10 &
    #sleep 2
done
wait

##
## To start the client, 
## tfmq-client -i taskEnv.lst -w 0 -r 1 -q tfmqtaskqueue
##
